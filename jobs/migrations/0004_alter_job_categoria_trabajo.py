# Generated by Django 5.1.6 on 2025-05-17 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_rename_description_job_descripcion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='categoria_trabajo',
            field=models.CharField(choices=[('diseño_grafico', 'Diseño gráfico'), ('ingenieria_informatica', 'Ingeniería informática'), ('marketing_digital', 'Marketing digital'), ('ingenierias', 'Ingenierias'), ('finanzas', 'Finanzas'), ('salud', 'Salud'), ('educacion', 'Educación'), ('administracion', 'Administración'), ('recursos_humanos', 'Recursos humanos')], default='ingenieria_informatica', max_length=100),
        ),
    ]
