#import from django library
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect                   #Used for redirection of webpages
from django.core.paginator import Paginator             #Used for implementing paginated lists
from django.conf import settings

#import from python library
import datetime

#import from project scripts
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
    #creates user, authenticates username for duplicates and hashes the password
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()


    context = {'form' :form}
    return render(request,'signUp.html')

def Crags(request):
    return render(request,'Crags.html')

def MyClimbs(request):
    return render(request,'MyClimbs.html')

def MyCommunity(request):
    posts = MBPost.objects.all().order_by('-time')
    posts_paginator = Paginator(posts, 5)
    page_no = request.GET.get('page')
    posts = posts_paginator.get_page(page_no)
    args = {'posts':posts}
    return render(request,'MyCommunity.html', args)

def MyCommunityCreate(request):
    message = request.POST.get("message")
    title = request.POST.get("title")
    time = datetime.datetime.now()
    args = {'postform': MBPostForm()}
    MBPost.objects.create(text=message, title=title, time=time)
    return redirect('MyCommunity')

def Settings(request):
    return render(request,'Settings.html')


def route(request): 

  context = {"google_api_key": settings.GOOGLE_API_KEY}
  return render(request, 'GoClimbApp/Templates/Crags.Crags.html', context)


def map(request):

	lat_a = request.GET.get("lat_a")
	long_a = request.GET.get("long_a")
	lat_b = request.GET.get("lat_b")
	long_b = request.GET.get("long_b")
	directions = Directions(
		lat_a= lat_a,
		long_a=long_a,
		lat_b = lat_b,
		long_b=long_b
		)

	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"lat_a": lat_a,
	"long_a": long_a,
	"lat_b": lat_b,
	"long_b": long_b,
	"origin": f'{lat_a}, {long_a}',
	"destination": f'{lat_b}, {long_b}',
	"directions": directions,

	}
	return render(request, 'GoClimbApp/Templates/Crags.Crags.html', context)
