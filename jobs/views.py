from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Job
from .forms import JobForm

def job_list(request):
    # Listado inicial de vacantes activas ordenadas por fecha
    jobs = Job.objects.filter(esta_activa=True).order_by('-fecha_publicacion')

    # Leer filtros desde GET
    categoria = request.GET.get('categoria_trabajo')
    tipo_empleo = request.GET.get('tipo_empleo')
    ubicacion = request.GET.get('ubicacion')
    nivel_experiencia = request.GET.get('nivel_experiencia')

    # Aplicar filtros si no se seleccionó "todos"
    if categoria and categoria != 'todos':
        jobs = jobs.filter(categoria_trabajo=categoria)

    if tipo_empleo and tipo_empleo != 'todos':
        jobs = jobs.filter(tipo_empleo=tipo_empleo)

    if ubicacion and ubicacion != 'todas':
        jobs = jobs.filter(ubicacion=ubicacion)

    if nivel_experiencia and nivel_experiencia != 'todos':
        jobs = jobs.filter(nivel_experiencia=nivel_experiencia)

    # Paginación
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categorias': [
            ("diseno_grafico", "Diseño gráfico"),
            ("ingenieria_informatica", "Ingeniería informática"),
            ("marketing_digital", "Marketing digital"),
            ("ingenierias", "Ingenierias"),
            ("finanzas", "Finanzas"),
            ("salud", "Salud"),
            ("educacion", "Educación"),
            ("administracion", "Administración"),
            ("recursos_humanos", "Recursos humanos"),
        ],
        'tipos_empleo': [
            ('tiempo_completo', 'Tiempo completo'),
            ('medio_tiempo', 'Medio tiempo'),
            ('remoto', 'Remoto'),
            
        ],
        'ubicaciones': ['Bogotá', 'Medellín', 'Cali', 'Remoto', 'Otra'],
        'niveles_experiencia': ['Entry', 'Mid', 'Junior', 'Senior'],
        'categoria_seleccionada': categoria or 'todos',
        'tipo_empleo_seleccionado': [
        ('tiempo_completo', 'Tiempo completo'),
        ('medio_tiempo', 'Medio tiempo'),
        ('contrato', 'Contrato'),
        ('pasantia', 'Pasantía'),
        ('remoto', 'Remoto')
        ],
        'ubicacion_seleccionada': ubicacion or 'todas',
        'nivel_experiencia_seleccionado': nivel_experiencia or 'todos',
        'jobs': page_obj,
    }

    return render(request, 'job_list.html', context)


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
