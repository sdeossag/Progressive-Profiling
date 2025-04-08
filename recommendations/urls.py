from django.urls import path
from .views import job_recommendations

urlpatterns = [
    path('', job_recommendations, name='recomendaciones'),
]
