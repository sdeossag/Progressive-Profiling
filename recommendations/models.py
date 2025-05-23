from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job
import json
import numpy as np

class JobLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} 👍 {self.job.titulo}"


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='recommended_to')
    score = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.username} → {self.job.titulo} ({self.score:.2f})"


class UserProfileEmbedding(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_embedding')
    embedding_json = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def set_embedding(self, embedding_array):
        self.embedding_json = json.dumps(embedding_array.tolist())

    def get_embedding(self):
        return np.array(json.loads(self.embedding_json))

    def __str__(self):
        return f"Embedding perfil: {self.user.username}"
