from django.shortcuts import render
from django.http import HttpResponse




# Create your views here.

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def signIn(request):
    return render(request,'signIn.html')

def signUp(request):
    return render(request,'signUp.html')

def Crags(request):
    return render(request,'Crags.html')

def MyClimbs(request):
    return render(request,'MyClimbs.html')

def MyCommunity(request):
    return render(request,'MyCommunity.html')

def Settings(request):
    return render(request,'Settings.html')



