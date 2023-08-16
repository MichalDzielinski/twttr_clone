from django.shortcuts import render, redirect
from .models import Profile
from django.contrib import messages

def home(request):
    context = {}
    return render(request, 'mitter/home.html', context)

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        context  ={'profiles': profiles}
        return render(request, 'mitter/profile_list.html', context)
    else:
        messages.success(request, ('You must be logged-in to see this page'))
        return redirect('home')