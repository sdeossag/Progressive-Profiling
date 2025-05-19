from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Importar el sistema de mensajes

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Cambios guardados con éxito!")  # Mensaje de éxito
            return redirect('profile_detail')  # Redirigir a la vista de detalles del perfil
        else:
            messages.error(request, "Hubo un error al guardar los cambios. Inténtalo nuevamente.")  # Mensaje de error
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profiles.html', {'form': form})

@login_required
def profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile_detail.html', {'profile': profile})
