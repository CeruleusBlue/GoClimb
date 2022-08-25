from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

from django.db import models




# Create your views here.

def index(request):
    return render(request,'index.html')

@login_required(login_url='signIn')
def home(request):
    return render(request,'home.html')

def signIn(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request,'signIn.html')

def signUp(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('signIn')

        context = {'form': form}
        return render(request,'signUp.html', context)


def logoutUser(request):
	logout(request)
	return redirect('signIn')


@login_required(login_url='signIn')
def Crags(request):
    return render(request,'Crags.html')



@login_required(login_url='signIn')
def MyClimbs(request):
    return render(request,'MyClimbs.html')



@login_required(login_url='signIn')
def MyCommunity(request):
    posts = MBPost.objects.all()
    args = {'posts':posts}
    return render(request,'MyCommunity.html', args)



@login_required(login_url='signIn')
def MyCommunityCreate(request):
    message = request.POST.get("message")
    args = {'postform': MBPostForm()}
    MBPost.objects.create(text=message)
    return MyCommunity(request)


@login_required(login_url='signIn')
def Settings(request):
    return render(request,'Settings.html')



