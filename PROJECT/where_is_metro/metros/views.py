from django.shortcuts import render

# Create your views here.
from .models import Stations


def home(request):
    stations=Stations.objects.all()
    return render(request, 'home.html',{'stations':stations})