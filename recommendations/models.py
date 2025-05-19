from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class JobLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='recommended_to')
    score = models.FloatField(default=0.0)  # Puntaje de similitud
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')  # Evita duplicados
        ordering = ['-score']  # Ordena por relevancia

    def __str__(self):
        return f"{self.user.username} → {self.job.titulo} ({self.score:.2f})"
