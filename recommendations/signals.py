# recommendations/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from sentence_transformers import SentenceTransformer
from .models import JobLike
from profiles.models import UserProfileEmbedding
import numpy as np
import json

@receiver(post_save, sender=JobLike)
def update_embedding_on_like(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    liked_jobs = JobLike.objects.filter(user=user).select_related('job')

    if not liked_jobs.exists():
        return

    profile_text = ' '.join([
        ' '.join(filter(None, [
            (job.titulo + ' ') * 2,
            job.categoria_trabajo or '',
            job.descripcion or '',
            job.requisitos or '',
            job.responsabilidades or '',
            job.habilidades_requeridas or '',
        ])) for job in [like.job for like in liked_jobs]
    ])

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(profile_text, convert_to_tensor=False)

    profile_embedding, created = UserProfileEmbedding.objects.get_or_create(user=user)
    profile_embedding.set_embedding(embedding)
    profile_embedding.save()
