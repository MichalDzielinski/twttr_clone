from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'mitter/home.html', context)
