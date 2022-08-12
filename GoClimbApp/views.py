from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import MBPost
from .forms import MBPostForm



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
    posts = MBPost.objects.all()
    args = {'posts':posts}
    return render(request,'MyCommunity.html', args)

def MyCommunityCreate(request):
    message = request.POST.get("message")
    args = {'postform': MBPostForm()}
    MBPost.objects.create(text=message)
    return MyCommunity(request)

def Settings(request):
    return render(request,'Settings.html')



