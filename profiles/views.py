from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')  # Asegúrate de crear esta vista luego
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profiles.html', {'form': form})

@login_required
def profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile_detail.html', {'profile': profile})
