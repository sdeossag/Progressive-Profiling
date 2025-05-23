from django.urls import path
from .views import job_recommendations, job_like
from . import views

urlpatterns = [
    path('', job_recommendations, name='recomendaciones'),
    path('job-like/<int:job_id>/', job_like, name='job_like'),
    path('<int:job_id>/like-and-similar/', views.like_and_show_similar_jobs, name='like_and_show_similar'),
]
