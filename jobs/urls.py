from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('crear/', views.job_create, name='job_create'),
    path('<int:job_id>/editar/', views.job_edit, name='job_edit'),
]
