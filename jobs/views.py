from django.shortcuts import render, get_object_or_404, redirect
from .models import Job
from .forms import JobForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def job_list(request):
    jobs = Job.objects.all().order_by('-date_posted') 

    return render(request, 'job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user  # Asociar con usuario actual
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'job_form.html', {'form': form, 'action': 'Crear'})

@login_required
def job_edit(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Opcional: restringir edición a quien creó la vacante
    if job.created_by != request.user:
        return HttpResponseForbidden("No tienes permiso para editar esta vacante.")

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)
    return render(request, 'job_form.html', {'form': form, 'action': 'Editar'})
