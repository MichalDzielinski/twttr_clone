from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Meep
from django.contrib import messages
from .forms import MeepForm, SignUpForm, UserUpdateForm, ProfilePicForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

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

def update_user(request):
    if request.user.is_authenticated:
        current_user  = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            current_user = user_form.save()
            profile_user = profile_form.save()
            login(request, current_user)
            messages.success(request, ('Your profile has been updated successfully!'))
            return redirect('home')

        context = {
            'user_form': user_form, 'profile_form': profile_form
        }
        return render(request, 'mitter/update_user.html', context)
    else:
        messages.success(request, ('You must be logged in to see this page'))
        return redirect('home')

def meep_like(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
   
    else:
        messages.success(request, ('You must be logged-in to see this'))
        return redirect('home')

def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(request, 'mitter/meep_show.html', {'meep': meep})
    else:
        messages.success(request, ('That meep does not exists!'))
        return redirect('home')



    context = {}
    return render(request, '', context)

