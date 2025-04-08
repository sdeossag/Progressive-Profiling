from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from jobs.models import Job
from profiles.models import Profile

def recommend_jobs_for_user(user, top_n=5):
    profile = Profile.objects.get(user=user)
    
    # Combina todos los datos relevantes del perfil
    user_profile_text = ' '.join([
        profile.skills or '',
        profile.interests or '',
        profile.career_goals or '',
        profile.values or '',
        profile.experience_level or '',
    ])
    
    jobs = Job.objects.all()
    job_texts = []
    job_ids = []
    
    for job in jobs:
        text = ' '.join([
            job.title or '',
            job.description or '',
            job.requirements or '',
            job.responsibilities or '',
        ])
        job_texts.append(text)
        job_ids.append(job.id)
    
    # Crea el corpus combinando el perfil + todas las vacantes
    corpus = [user_profile_text] + job_texts
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Calcula la similitud entre el perfil del usuario y cada vacante
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Ordena los resultados por puntaje de similitud
    top_indices = similarity_scores.argsort()[::-1][:top_n]
    recommended_job_ids = [job_ids[i] for i in top_indices]
    
    return Job.objects.filter(id__in=recommended_job_ids)
