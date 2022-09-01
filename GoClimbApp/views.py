#import from django library

    #import 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect                   #Used for redirection of webpages
from django.core.paginator import Paginator             #Used for implementing paginated lists
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import *
from .forms import *
class indexView(View):
    template_name = 'index.html'
    def get(self, request):
        return render(request, self.template_name)

class homeView(LoginRequiredMixin, View):
    login_url='signIn'
    template_name = 'home.html'
    def get(self, request):
        print(request.user.is_authenticated)
        return render(request, self.template_name)
class signInView(View):
    template_name = 'signIn.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
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
            return self.get(request)
        
def logoutUser(request):
        logout(request)
        return redirect('signIn')

class signUpView(View):
    template_name = 'signUp.html'
    form = CreateUserForm()
    context = {'form': form}

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        self.form = CreateUserForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            username = self.form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            userProfile.objects.create(userID=user)
            messages.success(request, 'Account was created for ' + username)
            return redirect('signIn')
        else:    
            return self.get(request)

class cragsView(LoginRequiredMixin, View):
    login_url='signIn'
    template_name = 'Crags.html'
    def get(self, request):
        return render(request, self.template_name)

class myClimbsView(LoginRequiredMixin, View):
    login_url='signIn'
    template_name = 'MyClimbs.html'
    def get(self, request):
        return render(request, self.template_name)

class myCommunityView(LoginRequiredMixin, View):
    login_url='signIn'
    template_name = 'MyCommunity.html'

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

class settingsView(LoginRequiredMixin, View):
    login_url='signIn'
    template_name = 'Settings.html'
    def get(self, request):
        return render(request, self.template_name)
