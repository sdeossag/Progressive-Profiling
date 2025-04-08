from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from profiles.models import Profile
from sentence_transformers import SentenceTransformer, util
import torch

@login_required
def job_recommendations(request):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        return render(request, 'recommendations.html', {
            'recommended_jobs': [],
            'error': 'No tienes un perfil completado.'
        })

    user_level = profile.experience_level.lower() if profile.experience_level else ''
    profile_text = f"{profile.career_goals} {profile.skills} {profile.interests} {profile.values}"

    jobs = Job.objects.filter(is_active=True)
    if not jobs.exists():
        return render(request, 'recommendations.html', {
            'recommended_jobs': [],
            'error': 'No hay vacantes disponibles.'
        })

    # Inicializar modelo de embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Puedes usar otro más potente si lo deseas

    # Obtener embeddings
    profile_embedding = model.encode(profile_text, convert_to_tensor=True)

    job_embeddings = []
    job_list = []
    for job in jobs:
        job_text = f"{job.title} {job.description} {job.requirements} {job.skills_required}"
        embedding = model.encode(job_text, convert_to_tensor=True)
        job_embeddings.append(embedding)
        job_list.append(job)

    # Calcular similitudes coseno
    similarities = util.cos_sim(profile_embedding, torch.stack(job_embeddings)).squeeze()

    # Umbral de similitud (ajustable)
    threshold = 0.45

    # Emparejar empleos con puntaje
    scored_jobs = [
        (score.item(), job)
        for score, job in zip(similarities, job_list)
        if score >= threshold
    ]

    # Ordenar por similitud descendente
    scored_jobs.sort(reverse=True, key=lambda x: x[0])

    recommended_jobs = [job for _, job in scored_jobs]

    return render(request, 'recommendations.html', {
        'recommended_jobs': recommended_jobs,
        'error': None if recommended_jobs else "No se encontraron coincidencias relevantes."
    })
