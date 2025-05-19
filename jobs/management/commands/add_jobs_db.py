from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from jobs.models import Job
import csv
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Carga empleos desde empleos_medellin.csv al modelo Job'

    def handle(self, *args, **kwargs):
        # Ruta al archivo CSV
        csv_file_path = os.path.join('jobs', 'management', 'commands', 'admin_empleos.csv')

        # Obtener el usuario creador
        try:
            user = User.objects.get(username='asus')
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR('No se encontró el usuario "asus".'))
            return

        # Abrir el CSV
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            inserted_count = 0

            
            for row in reader:
                if row is None or all(value is None for value in row.values()):
                    continue  # Salta filas completamente vacias

                titulo = row.get('Titulo', '').strip() if row.get('Titulo') else ''
                empresa = row.get('Empresa', '').strip() if row.get('Empresa') else ''

                if not titulo or not empresa:
                    print('Fila sin titulo o empresa, saltada:', row)
                    continue

                print(f"Revisando empleo: {titulo} en {empresa}")

                exist = Job.objects.filter(
                    titulo=titulo,
                    empresa=empresa,
                    ubicacion=row.get('Ubicacion', '').strip(),
                    descripcion=row.get('Descripcion', '').strip(),
                    responsabilidades=row.get('Responsabilidades', '').strip(),
                    requisitos=row.get('Requisitos', '').strip(),
                ).first()

                if not exist:
                    print("No existe, creando...")
                    Job.objects.create(
                        creada_por=user,
                        titulo=titulo,
                        empresa=empresa,
                        ubicacion=row.get('Ubicacion', 'Medellin').strip(),
                        descripcion=row.get('Descripcion', '').strip(),
                        responsabilidades=row.get('Responsabilidades', '').strip(),
                        requisitos=row.get('Requisitos', '').strip(),
                        rango_salarial=row.get('Rango salarial', '').strip(),
                        tipo_empleo=row.get('Tipo de empleo', 'tiempo_completo').strip(),
                        nivel_experiencia=row.get('Nivel de experiencia', 'entry').strip(),
                        habilidades_requeridas=row.get('Habilidades requeridas', '').strip(),
                        categoria_trabajo=row.get('Categoria de trabajo', 'otro').strip(),
                        esta_activa=row.get('Estado del empleo', 'Activo').strip().lower() in ('activo', 'true', '1'),
                        fecha_publicacion=timezone.now()
                    )
                    inserted_count += 1
                else:
                    print("Ya existe, omitido.")


        self.stdout.write(self.style.SUCCESS(f'{inserted_count} empleos cargados correctamente.'))
