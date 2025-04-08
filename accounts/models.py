from jobs.models import Job
from django.shortcuts import render, get_object_or_404, redirect

def home(request):
    jobs = Job.objects.order_by('-published_at')[:5]  # Últimas 5 vacantes
    return render(request, 'home.html', {'jobs': jobs})
