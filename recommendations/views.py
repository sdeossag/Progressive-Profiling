from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from .recommender import recommend_jobs_for_user, recommend_similar_jobs_for_job
from .models import Recommendation, Job, JobLike
from django.http import JsonResponse

@login_required
def job_recommendations(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return render(request, 'recommendations.html', {
            'recommended_jobs': [],
            'error': 'No tienes un perfil completado.'
        })

    if not profile.objetivos_profesionales:
        return render(request, 'recommendations.html', {
            'recommended_jobs': [],
            'error': 'Por favor completa tu objetivo profesional para recibir recomendaciones.'
        })

    # Siempre regenerar las recomendaciones para tenerlas actualizadas
    recommend_jobs_for_user(request.user)

    # Obtener recomendaciones guardadas
    recommendations = Recommendation.objects.filter(user=request.user).select_related('job').order_by('-score')[:15]
    print(f"Cantidad recomendaciones: {len(recommendations)}")  # o usar logger.info(...)


    recommended_jobs = [rec.job for rec in recommendations]

    return render(request, 'recommendations.html', {
        'recommended_jobs': recommended_jobs,
        'error': None if recommended_jobs else 'No se encontraron coincidencias relevantes.'
    })

@login_required
def job_like(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    # Registrar o actualizar la recomendación (como "like")
    Recommendation.objects.get_or_create(user=request.user, job=job)
    return redirect('recomendaciones')


@login_required
def like_and_show_similar_jobs(request, job_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    job = get_object_or_404(Job, id=job_id)
    JobLike.objects.get_or_create(user=request.user, job=job)


    similar = recommend_similar_jobs_for_job(job, top_n=6)
    result = [{
        "id": j.id,
            "titulo": j.titulo,
            "empresa": j.empresa,
            "ubicacion": j.ubicacion,
            "descripcion": j.descripcion[:200],
            "tipo_empleo": j.get_tipo_empleo_display(),
            "nivel_experiencia": j.get_nivel_experiencia_display(),
    } for j, _ in similar]

    return JsonResponse({'similar_jobs': result})

