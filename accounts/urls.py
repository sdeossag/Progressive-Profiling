from django.urls import path, include
from . import views

urlpatterns = [
    path('signupaccount/', views.signupaccount, name='signupaccount'),
    path('loginaccount/', views.loginaccount, name='loginaccount'),
    path('logoutaccount/', views.logoutaccount, name='logoutaccount'),
    path('', views.home, name='home'),
    path('perfil/', include('profiles.urls')),
    path('perfil/editar/', views.edit_profile, name='edit_profile'),
    path('recomendaciones/', include('recommendations.urls')),


]