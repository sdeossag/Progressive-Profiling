from django.urls import path
from . import views

urlpatterns = [
    path('perfil/editar/', views.edit_profile, name='edit_profile'),
    path('perfil/', views.profile_detail, name='profile_detail'),
]
