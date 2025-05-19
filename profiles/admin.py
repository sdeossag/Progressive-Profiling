# admin.py

from django.contrib import admin
from .models import Profile

# Registra el modelo Profile para que aparezca en el admin
admin.site.register(Profile)