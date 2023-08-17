from django.shortcuts import render, redirect
from .models import Profile, Meep
from django.contrib import messages

def home(request):
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
        meeps = Meep.objects.filter(user_id=pk)


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









