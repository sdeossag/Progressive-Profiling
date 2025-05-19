from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

from jobs.models import Job
from profiles.models import Profile
from .models import Recommendation, JobLike


def recommend_jobs_for_user(user, top_n=5):
    # Construir texto del perfil usando trabajos que le gustaron
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
        # Si no hay likes, usar el perfil
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

    # Obtener trabajos activos
    jobs = Job.objects.filter(esta_activa=True)
    if not jobs.exists():
        return []

    job_texts = []
    job_objects = []

    for job in jobs:
        job_text = ' '.join(filter(None, [
            (job.titulo + ' ') * 2,
            job.categoria_trabajo or '',
            job.descripcion or '',
            job.requisitos or '',
            job.responsabilidades or '',
            job.habilidades_requeridas or '',
        ]))
        job_texts.append(job_text)
        job_objects.append(job)

    # Vector TF-IDF
    corpus = [user_profile_text] + job_texts
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
    tfidf_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Vector semántico con Sentence Transformers
    profile_embedding = sbert_model.encode(user_profile_text, convert_to_tensor=True)
    job_embeddings = sbert_model.encode(job_texts, convert_to_tensor=True)

    embedding_scores = util.cos_sim(profile_embedding, job_embeddings).squeeze().cpu().numpy()

    # Combinar scores (ajustable)
    combined_scores = (0.6 * embedding_scores) + (0.4 * tfidf_scores)

    # Borrar recomendaciones anteriores
    Recommendation.objects.filter(user=user).delete()

    # Guardar recomendaciones nuevas
    for i in combined_scores.argsort()[::-1][:top_n]:
        score = combined_scores[i]
        if score > 0.2:
            Recommendation.objects.create(user=user, job=job_objects[i], score=score)

    return Recommendation.objects.filter(user=user).order_by('-score')[:top_n]
