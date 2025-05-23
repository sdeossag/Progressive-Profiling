from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

from jobs.models import Job, JobEmbedding
import numpy as np
import pickle
import os
from django.conf import settings


class Command(BaseCommand):
    help = "Genera y actualiza los embeddings TF-IDF y SBERT para los trabajos activos"

    def handle(self, *args, **kwargs):
        self.stdout.write("Cargando modelo SentenceTransformer...")
        sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

        self.stdout.write("Obteniendo trabajos activos...")
        jobs = Job.objects.filter(esta_activa=True)

        job_texts = []
        job_list = []

        for job in jobs:
            text = ' '.join(filter(None, [
                (job.titulo + ' ') * 2,
                job.categoria_trabajo or '',
                job.descripcion or '',
                job.requisitos or '',
                job.responsabilidades or '',
                job.habilidades_requeridas or '',
            ]))
            job_texts.append(text)
            job_list.append(job)

        self.stdout.write(f"Generando matriz TF-IDF para {len(job_texts)} trabajos...")
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(job_texts)

        # Guardar vectorizador TF-IDF para usar luego en las recomendaciones
        vectorizer_path = os.path.join(settings.BASE_DIR, 'recommendations', 'tfidf_vectorizer.pkl')
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vectorizer, f)
        self.stdout.write(f"Vectorizador TF-IDF guardado en: {vectorizer_path}")

        self.stdout.write("Generando embeddings semánticos SBERT...")
        sentence_embeddings = sbert_model.encode(job_texts)

        self.stdout.write("Guardando embeddings en la base de datos...")
        for i, job in enumerate(job_list):
            emb_obj, created = JobEmbedding.objects.get_or_create(job=job)
            emb_obj.set_tfidf_vector(tfidf_matrix[i])
            emb_obj.set_sentence_embedding(sentence_embeddings[i])
            emb_obj.save()

        self.stdout.write(self.style.SUCCESS("Embeddings actualizados correctamente."))
