#import from django library

    #import 

from math import log
import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect                   #Used for redirection of webpages
from django.core.paginator import Paginator             #Used for implementing paginated lists
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
import json
from .serializers import *
import datetime

from .models import *
from .models import userProfile
from .forms import *
import json, urllib

class indexView(View):
    template_name = 'index.html'
    def get(self, request):
        return render(request, self.template_name)


class homeView(LoginRequiredMixin, View):
    login_url='signIn'
    template_name = 'home.html'
    def get(self, request):
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


#user registration page 
class signUpView(View):
    
    template_name = 'signUp.html'
    form = CreateUserForm()
    context = {'form': form}

    def get(self, request):
        
        #redirect user to home page after user authentication
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        
        #create user with Django's CreateUserForm
        self.form = CreateUserForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            username = self.form.cleaned_data.get('username')
            
            #assigning user their provided username
            user = User.objects.get(username=username)
            
            #assign a unique userID to each user 
            userProfile.objects.create(userID=user)
            
            #upon successfully creating new user, system flashes a message as "Account was created for user_name"
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
        return render(request, self.template_name, {'level': userProfile.objects.get(userID=request.user).level})

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
        MBPost.objects.create(text=message, title=title, time=time, FKUserProfile=userProfile.objects.get(userID=request.user))
        return self.get(request)

class likePostView(LoginRequiredMixin, View):
    def get(self, request):
        post = MBPost.objects.get(id=request.GET.get("id"))
        try:
            postLikeStatus = MBPostLikeStatus.objects.get(
            FKUserProfile = userProfile.objects.get(userID=request.user), 
            FKMBPost = post)
            postLikeStatus.isLiked = not postLikeStatus.isLiked
            postLikeStatus.save(update_fields=['isLiked'])
        except MBPostLikeStatus.DoesNotExist:
            postLikeStatus = MBPostLikeStatus(
            FKUserProfile = userProfile.objects.get(userID=request.user), 
            FKMBPost = post, isLiked = True)
            postLikeStatus.save()
        finally:
            return redirect('MyCommunity')

class settingsView(LoginRequiredMixin, View):
    login_url='signIn'
    template_name = 'Settings.html'
    def get(self, request):
        return render(request, self.template_name)
    
    
   #####################################################
    # New view of all crags relocate it as you want...
   #####################################################
def Crags(request):
    return render(request,'Crags.html')


#Crags page with real time weather update and potential hazard warnings 
#Requires user to login
class Crags1(LoginRequiredMixin, View):
    
    
    login_url='signIn'
    template_name = 'Crags1.html'


    def get(self, request):
        #empty python dictionary created to later store the values returned from the weather API call 
        data = {}

        #a real time weather API is acquired from OpenWeatherMap 
        #the returned data is in a json data format and is loaded as a Python dictionary 
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=Wollongong&units=metric&appid=6e1079025f4832f4f4947ebbf8276420').read()
        list_of_data = json.loads(source)


        #the data dictionary is populated with weather data attributes considered necessary for the project
        data = {
            "temp": str(list_of_data['main']['temp']) + ' °C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            'main': str(list_of_data['weather'][0]['main']),
            'description': str(list_of_data['weather'][0]['description']),
            'icon': list_of_data['weather'][0]['icon'],
            "wind": str(list_of_data['wind']['speed']) + ' m/s'
        }
        

        #Creating Hazard reports
        
        #potential wind hazard is reported in case of high wind speed  
        if float(list_of_data['wind']['speed']) > 2:
            data["windWarning"] = 'Wind Hazard!'
        
        #Chances of rain forecasted if the sky is cloudy
        if str(list_of_data['weather'][0]['main']) == 'Clouds':
            data["RainForecasted"] = 'Rain Forecasted!'
            
        #potential rain hazard is reported in case of rain 
        if str(list_of_data['weather'][0]['main']) == 'Rain':
            data["rainWarning"] = 'Rain Hazard!'
            
        
        return render(request, self.template_name, data)

    def post(self, request):
        
        return self.get(request)



class Crags2(LoginRequiredMixin, View):
    login_url='signIn'
    template_name = 'Crags2.html'
    def get(self, request):
        if(len(request.GET)>0):
            routes = None
            data = request.GET
            rating = int(data['Rating'])
            grade = int(data['Grade'])
            length = data['Rope Length']
            if(length == 'True'):
                routes = cragRoute.objects.filter(rating__gte=rating, grade__gte=grade, length__gte = 25)
            else:
                routes = cragRoute.objects.filter(rating__gte=rating, grade__gte=grade, length__lte = 25)

            serialize_routes=CragRouteSerializer(routes,many=True)
            data =  serialize_routes.data
            
            # for path in routes:
            result=json.dumps(serialize_routes.data)            
            return render(request, 'Crags3.html', {'routes':result, 'length':len(routes),'imgs':routes})
        return render(request, self.template_name)
class Crags3(LoginRequiredMixin, View):
    login_url='signIn'
    template_name = 'Crags3.html'
    def get(self, request):
        return render(request, self.template_name)

def Crags4(request):
    return render(request,'Crags4.html')

class Crags5(LoginRequiredMixin, View):
    login_url='signIn'
    template_name = 'Crags5.html'
    def get(self, request):
        if(len(request.GET)==2):
            grade = int(request.GET['Grade'])
            rating = int(request.GET['Rating'])
            increase = int(log(grade*rating))
            profile = userProfile.objects.get(userID=request.user)
            previousLevel = profile.level
            profile.level+=increase
            profile.save(update_fields=["level"])
            return redirect('MyClimbs') 
        return render(request, self.template_name)
        
def SavedCrag(request):
    return render(request,'savedCrags.html')
###########################################################

