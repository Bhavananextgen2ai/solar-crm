from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def add_installation(request):
    return render(request, "installations/add_installation.html")
