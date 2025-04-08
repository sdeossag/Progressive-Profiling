from django.db import models
from django.contrib.auth.models import User

EXPERIENCE_LEVEL_CHOICES = [
    ('entry', 'Entry'),
    ('junior', 'Junior'),
    ('mid', 'Mid'),
    ('senior', 'Senior'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    career_goals = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    values = models.TextField(null=True, blank=True)
    experience_level = models.CharField(
        max_length=100,
        choices=EXPERIENCE_LEVEL_CHOICES,
        null=True,
        blank=True,
        default='entry'
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
