from django.db import models
from django.contrib.auth.models import User
class Job(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    employment_type = models.CharField(
        max_length=50,
        choices=[
            ('full_time', 'Tiempo completo'),
            ('part_time', 'Medio tiempo'),
            ('contract', 'Contrato'),
            ('internship', 'Pasantía'),
            ('remote', 'Remoto'),
        ]
    )
    experience_level = models.CharField(
        max_length=50,
        choices=[
            ('entry', 'Entry'),
            ('junior', 'Junior'),
            ('mid', 'Mid'),
            ('senior', 'Senior'),
        ]
    )
    skills_required = models.TextField(blank=True, help_text="Lista separada por comas")
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} en {self.company}"
