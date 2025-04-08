from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from jobs.models import Job
import json
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Carga empleos desde empleos_medellin.json al modelo Job'

    def handle(self, *args, **kwargs):
        # Ruta al archivo JSON
        json_file_path = os.path.join('jobs', 'management', 'commands', 'empleos_medellin.json')

        # Cargar el archivo
        with open(json_file_path, 'r', encoding='utf-8') as file:
            jobs = json.load(file)

        # Obtener el usuario creador
        try:
            user = User.objects.get(username='asus')
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR('No se encontró el usuario "asus".'))
            return

        # Insertar empleos
        inserted_count = 0
        for job in jobs:
            fields = job['fields']
            title = fields['title']
            company = fields['company']

            exist = Job.objects.filter(title=title, company=company).first()

            if not exist:
                Job.objects.create(
                    title=title,
                    company=company,
                    location=fields.get('location', 'Medellín'),
                    description=fields.get('description', ''),
                    responsibilities=fields.get('responsibilities', ''),
                    requirements=fields.get('requirements', ''),
                    salary_range=fields.get('salary_range', ''),
                    employment_type=fields.get('employment_type', 'full_time'),
                    experience_level=fields.get('experience_level', 'entry'),
                    skills_required=fields.get('skills_required', ''),
                    date_posted=fields.get('date_posted', timezone.now()),
                    is_active=fields.get('is_active', True),
                    created_by=user
                )
                inserted_count += 1

        self.stdout.write(self.style.SUCCESS(f'{inserted_count} empleos cargados correctamente.'))

