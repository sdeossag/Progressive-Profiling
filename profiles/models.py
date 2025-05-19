# models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    CATEGORIAS_TRABAJO = [
        ('tecnologia', 'Tecnología'),
        ('marketing', 'Marketing'),
        ('diseño', 'Diseño'),
        ('finanzas', 'Finanzas'),
        ('educacion', 'Educación'),
        ('salud', 'Salud'),
        ('ingenieria', 'Ingeniería'),
        ('legal', 'Legal'),
        ('recursos_humanos', 'Recursos Humanos'),
    ]
    
    DISPONIBILIDAD_CHOICES = [
        ('inmediata', 'Inmediata'),
        ('1_mes', '1 Mes'),
        ('2_meses', '2 Meses'),
        ('mas_de_2_meses', 'Más de 2 meses'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objetivos_profesionales = models.TextField(blank=True)
    categoria_trabajo = models.CharField(max_length=50, choices=CATEGORIAS_TRABAJO, blank=True)
    nivel_experiencia = models.CharField(max_length=50, choices=[
        ('entry', 'Entry'),
        ('junior', 'Junior'),
        ('mid', 'Mid'),
        ('senior', 'Senior'),
    ], blank=True)
    habilidades = models.TextField(blank=True)
    intereses = models.TextField(blank=True)
    valores = models.TextField(blank=True)
    
    # Nuevos campos
    educacion_maxima = models.CharField(max_length=255, blank=True, null=True)
    certificaciones = models.TextField(blank=True, null=True)
    tipo_trabajo_preferido = models.CharField(max_length=100, choices=[
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
        ('presencial', 'Presencial')
    ], blank=True, null=True)
    disponibilidad = models.CharField(max_length=100, choices=DISPONIBILIDAD_CHOICES, blank=True, null=True)
    idiomas_hablados = models.TextField(blank=True, null=True)

    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
