from django.contrib import admin
from django.urls import path, include
from accounts import views as accountsViews
from django.conf import settings
from django.conf.urls.static import static  # Importa static aquí


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accountsViews.home),
    path('accounts/', include('accounts.urls')),
    path('', include('profiles.urls')),
    path('jobs/', include('jobs.urls')),
    path('recomendaciones/', include('recommendations.urls')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

