from django.db import models
from django.contrib.auth.models import User
import pickle


class Job(models.Model):
    CATEGORIAS_TRABAJO = [
        ("diseno_grafico", "Diseño gráfico"),
        ("ingenieria_informatica", "Ingeniería informática"),
        ("marketing_digital", "Marketing digital"),
        ("ingenierias", "Ingenierias"),
        ("finanzas", "Finanzas"),
        ("salud", "Salud"),
        ("educacion", "Educación"),
        ("administracion", "Administración"),
        ("recursos_humanos", "Recursos humanos"),
    ]

    TIPO_EMPLEO = [
        ('tiempo_completo', 'Tiempo completo'),
        ('medio_tiempo', 'Medio tiempo'),
        ('contrato', 'Contrato'),
        ('pasantia', 'Pasantía'),
        ('remoto', 'Remoto'),
    ]

    NIVEL_EXPERIENCIA = [
        ('entry', 'Entry'),
        ('junior', 'Junior'),
        ('mid', 'Mid'),
        ('senior', 'Senior'),
    ]

    creada_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vacantes', blank=True, null=True)
    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=100)
    descripcion = models.TextField()
    responsabilidades = models.TextField(blank=True)
    requisitos = models.TextField(blank=True)
    rango_salarial = models.CharField(max_length=100, blank=True)

    tipo_empleo = models.CharField(
        max_length=50,
        choices=TIPO_EMPLEO
    , default='tiempo_completo'
    )
    nivel_experiencia = models.CharField(
        max_length=50,
        choices=NIVEL_EXPERIENCIA
    , default='entry'
    )
    habilidades_requeridas = models.TextField(blank=True, help_text="Lista separada por comas")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    esta_activa = models.BooleanField(default=True)

    categoria_trabajo = models.CharField(
        max_length=100,
        choices=CATEGORIAS_TRABAJO,
        default="ingenieria_informatica"
    )

    def __str__(self):
        return f"{self.titulo} en {self.empresa}"


class JobEmbedding(models.Model):
    job = models.OneToOneField('Job', on_delete=models.CASCADE, related_name='embedding')
    tfidf_vector = models.BinaryField()
    sentence_embedding = models.BinaryField()
    updated_at = models.DateTimeField(auto_now=True)

    def set_tfidf_vector(self, vector):
        self.tfidf_vector = pickle.dumps(vector)

    def get_tfidf_vector(self):
        return pickle.loads(self.tfidf_vector)

    def set_sentence_embedding(self, vector):
        self.sentence_embedding = pickle.dumps(vector)

    def get_sentence_embedding(self):
        return pickle.loads(self.sentence_embedding)

    def __str__(self):
        return f"Embeddings de {self.job.titulo}"