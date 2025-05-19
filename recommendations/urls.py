from django.urls import path
from .views import job_recommendations, job_like

urlpatterns = [
    path('', job_recommendations, name='recomendaciones'),
    path('job-like/<int:job_id>/', job_like, name='job_like'),
]
