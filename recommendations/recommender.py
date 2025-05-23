import os
import pickle
import numpy as np
from collections import defaultdict
from scipy.sparse import vstack
from sklearn.metrics.pairwise import cosine_similarity as cos_sim_np
from sentence_transformers import SentenceTransformer

from django.conf import settings

from jobs.models import JobEmbedding
from profiles.models import Profile
from .models import Recommendation, JobLike, UserProfileEmbedding


def recommend_jobs_for_user(user, top_n=9):
    liked_jobs = JobLike.objects.filter(user=user).select_related('job')

    if liked_jobs.exists():
        user_profile_text = ' '.join([
            ' '.join(filter(None, [
                (job.titulo + ' ') * 2,
                job.categoria_trabajo or '',
                job.descripcion or '',
                job.requisitos or '',
                job.responsabilidades or '',
                job.habilidades_requeridas or '',
            ])) for job in [like.job for like in liked_jobs]
        ])
    else:
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return []

        if not profile.objetivos_profesionales:
            return []

        user_profile_text = ' '.join(filter(None, [
            profile.categoria_trabajo or '',
            profile.habilidades or '',
            profile.intereses or '',
            profile.objetivos_profesionales or '',
            profile.valores or '',
            profile.nivel_experiencia or '',
        ]))

    embeddings_qs = JobEmbedding.objects.select_related('job').all()
    if not embeddings_qs.exists():
        return []

    job_objects = []
    tfidf_vectors = []
    sentence_embeddings = []

    for emb in embeddings_qs:
        job_objects.append(emb.job)
        tfidf_vectors.append(emb.get_tfidf_vector())
        sentence_embeddings.append(emb.get_sentence_embedding())

    tfidf_matrix = vstack(tfidf_vectors)
    sentence_embeddings = np.vstack(sentence_embeddings)

    vectorizer_path = os.path.join(settings.BASE_DIR, 'recommendations', 'tfidf_vectorizer.pkl')
    with open(vectorizer_path, 'rb') as f:
        tfidf_vectorizer = pickle.load(f)

    user_tfidf = tfidf_vectorizer.transform([user_profile_text])

    try:
        profile_embedding_obj = UserProfileEmbedding.objects.get(user=user)
        profile_embedding = profile_embedding_obj.get_embedding()
    except UserProfileEmbedding.DoesNotExist:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        profile_embedding = model.encode(user_profile_text, convert_to_tensor=False)
        profile_embedding_obj = UserProfileEmbedding(user=user)
        profile_embedding_obj.set_embedding(profile_embedding)
        profile_embedding_obj.save()

    tfidf_scores = cos_sim_np(user_tfidf, tfidf_matrix).flatten()
    embedding_scores = cos_sim_np([profile_embedding], sentence_embeddings).flatten()
    combined_scores = (0.8 * embedding_scores) + (0.2 * tfidf_scores)

    excluded_ids = set(
        Recommendation.objects.filter(user=user).values_list('job_id', flat=True)
    ).union(
        JobLike.objects.filter(user=user).values_list('job_id', flat=True)
    )

    Recommendation.objects.filter(user=user).delete()

    MAX_SIMILARITY_BETWEEN_JOBS = 0.90
    top_k = 100
    preselected = []

    for i in combined_scores.argsort()[::-1]:
        job = job_objects[i]
        if job.id in excluded_ids:
            continue
        score = combined_scores[i]
        if score < 0.1:
            continue
        preselected.append((job, sentence_embeddings[i], score))
        if len(preselected) >= top_k:
            break

    category_groups = defaultdict(list)
    for job, emb, score in preselected:
        category = job.categoria_trabajo or 'Sin categoría'
        category_groups[category].append((job, emb, score))

    selected = []
    selected_embeddings = []
    round_robin = True

    while round_robin and len(selected) < top_n:
        round_robin = False
        for category in list(category_groups.keys()):
            if not category_groups[category]:
                continue
            job, emb, score = category_groups[category].pop(0)

            if any(cos_sim_np([emb], [e])[0][0] > MAX_SIMILARITY_BETWEEN_JOBS for e in selected_embeddings):
                continue

            Recommendation.objects.create(user=user, job=job, score=score)
            selected.append(job)
            selected_embeddings.append(emb)
            round_robin = True
            if len(selected) >= top_n:
                break

    return Recommendation.objects.filter(user=user).order_by('-score')[:top_n]


def recommend_similar_jobs_for_job(job, top_n=6):
    embeddings_qs = JobEmbedding.objects.select_related('job').all()
    if not embeddings_qs.exists():
        return []

    job_objects = []
    sentence_embeddings = []

    for emb in embeddings_qs:
        job_objects.append(emb.job)
        sentence_embeddings.append(emb.get_sentence_embedding())

    sentence_embeddings = np.vstack(sentence_embeddings)

    try:
        job_embedding = JobEmbedding.objects.get(job=job).get_sentence_embedding()
    except JobEmbedding.DoesNotExist:
        return []

    embedding_scores = cos_sim_np([job_embedding], sentence_embeddings).flatten()

    results = []
    for i in embedding_scores.argsort()[::-1]:
        if job_objects[i].id != job.id:
            results.append((job_objects[i], embedding_scores[i]))
        if len(results) >= top_n:
            break

    return results

