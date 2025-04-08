from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.db import IntegrityError
from jobs.models import Job


# Create your views here.
def home (request):
    return render(request, 'home.html')

def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html', {
                    'form': UserCreationForm(),
                    'error': 'Username already taken. Choose a new username.'})

def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', 
                      {'form': AuthenticationForm()})
    else:
        user = authenticate(request, 
                            username=request.POST['username'], 
                            password=request.POST['password'])
        
        if user is None:
            return render(request, 'loginaccount.html', 
                          {'form': AuthenticationForm(), 
                           'error': 'username and password do not match'})
        else:
            login(request, user)
            return redirect('home')            

def logoutaccount(request):
    logout(request)
    return redirect('home')

def edit_profile(request):
    return render(request, 'edit_profiles.html')

def home(request):
    jobs = Job.objects.all().order_by('-date_posted')[:6]
    return render(request, 'home.html', {'jobs': jobs})