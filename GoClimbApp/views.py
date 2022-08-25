#import from django library
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator             #Used for implementing paginated lists

#import from python library
import datetime

#import from project scripts
from .models import MBPost



# Create your views here.

class indexView(View):
    template_name = 'index.html'
    def get(self, request):
        return render(request, self.template_name)

class homeView(View):
    template_name = 'home.html'
    def get(self, request):
        return render(request, self.template_name)

class signInView(View):
    template_name = 'signIn.html'
    def get(self, request):
        return render(request, self.template_name)

class signUpView(View):
    template_name = 'signUp.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name, kwargs)
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        context = {'form' :form}
        return self.get(request, context=context)

class cragsView(View):
    template_name = 'Crags.html'
    def get(self, request):
        return render(request, self.template_name)

class myClimbsView(View):
    template_name = 'MyClimbs.html'
    def get(self, request):
        return render(request, self.template_name)

class myCommunityView(View):
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

class settingsView(View):
    template_name = 'Settings.html'
    def get(self, request):
        return render(request, self.template_name)


