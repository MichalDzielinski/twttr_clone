from django.shortcuts import render, redirect
from .models import Profile, Meep
from django.contrib import messages
from .forms import MeepForm, SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms

def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if form.is_valid():
            meep = form.save(commit = False)
            meep.user = request.user
            meep.save()
            messages.success(request, ('Meep added successfully'))
            return redirect('home')

        meeps = Meep.objects.all().order_by('-created_at')
        context = {'meeps': meeps,  'form': form}
        return render(request, 'mitter/home.html', context)
    else:
        meeps = Meep.objects.all().order_by('-created_at')
        context = {'meeps': meeps}
        return render(request, 'mitter/home.html', context)

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        context  ={'profiles': profiles}
        return render(request, 'mitter/profile_list.html', context)
    else:
        messages.success(request, ('You must be logged-in to see this page'))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by('-created_at')


        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        context = {'profile': profile, 'meeps': meeps}
        return render(request, 'mitter/profile.html', context )

    else:
        messages.success(request, ('You have to be logged in to see this page'))
        return redirect('home')

def login_user(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,  user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('There was some error during your login'))
            return redirect('login')
    else:
        return render(request, 'mitter/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('home')

def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']

            user = authenticate(username = username, password=password)
            login(request, user)
            messages.success(request, 'You have been registered successfully')
            return redirect('home')
    return render(request, 'mitter/register.html', {'form': form})






