from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Job
from .forms import JobForm

def job_list(request):
    jobs = Job.objects.all().order_by('-fecha_publicacion')
    
    # Paginación: mostrar 10 empleos por página
    paginator = Paginator(jobs, 10)  # 10 por página
    page_number = request.GET.get('page')  # Obtener número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtener la página actual

    return render(request, 'job_list.html', {'jobs': page_obj})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.creada_por = request.user  # Asociar con el usuario actual
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'job_form.html', {'form': form, 'action': 'Crear'})

@login_required
def job_edit(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.creada_por != request.user:
        return HttpResponseForbidden("No tienes permiso para editar esta vacante.")

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)
    return render(request, 'job_form.html', {'form': form, 'action': 'Editar'})
