#import from django library
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect                   #Used for redirection of webpages
from django.core.paginator import Paginator             #Used for implementing paginated lists
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#import from python library
import datetime

#import from project scripts
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

# Create your views here.
def index(request):
    return render(request,'index.html')

class indexView(View):
    template_name = 'index.html'
    def get(self, request):
        return render(request, self.template_name)

class homeView(View, LoginRequiredMixin):
    template_name = 'home.html'
    login_url='signIn'

    def get(self, request):
        return render(request, self.template_name)

class signInView(View):
    template_name = 'signIn.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
        context = {}
        return self.get(request)

class signUpView(View):
    template_name = 'signUp.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, self.template_name, kwargs)
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('signIn')
        context = {'form' :form}
        return self.get(request, context=context)

class cragsView(View, LoginRequiredMixin):
    template_name = 'Crags.html'
    login_url='signIn'

    def get(self, request):
        return render(request, self.template_name)

class myClimbsView(View, LoginRequiredMixin):
    template_name = 'MyClimbs.html'
    login_url='signIn'

    def get(self, request):
        return render(request, self.template_name)

class myCommunityView(View, LoginRequiredMixin):
    template_name = 'MyCommunity.html'
    login_url='signIn'

    def get(self, request):
        posts = MBPost.objects.all().order_by('-time')
        posts_paginator = Paginator(posts, 5)
        page_no = request.GET.get('page')
        posts = posts_paginator.get_page(page_no)
        args = {'posts':posts}
        return render(request,self.template_name, args)
    
    def post(self, request):
        message = request.POST.get("message")
        title = request.POST.get("title")
        time = datetime.datetime.now()
        MBPost.objects.create(text=message, title=title, time=time)
        return self.get(request)

class settingsView(View, LoginRequiredMixin):
    template_name = 'Settings.html'
    login_url='signIn'

    def get(self, request):
        return render(request, self.template_name)


@login_required(login_url='signIn')
def logoutUser(request):
	logout(request)
	return redirect('signIn')