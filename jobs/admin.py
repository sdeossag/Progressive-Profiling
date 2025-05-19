from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'ubicacion', 'tipo_empleo', 'nivel_experiencia', 'fecha_publicacion', 'esta_activa')
    search_fields = ('titulo', 'empresa', 'ubicacion')
    list_filter = ('tipo_empleo', 'nivel_experiencia', 'esta_activa')
    ordering = ('-fecha_publicacion',)
