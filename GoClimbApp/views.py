#Import from Python
from math import log
import datetime, json, urllib

#Import from Django Shortcuts
from django.shortcuts import render, redirect

#Import from Django Views
from django.views import View

#Import from Django Core
#Used for implementing paginated lists
from django.core.paginator import Paginator  

#Import from Django Contrib
from django.contrib import messages           
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

#Import from Local Directory
from .serializers import *
from .models import *
from .forms import *

class indexView(View):
    """Index Page View Class"""
    template_name = 'index.html'
    def get(self, request):
        """Renders the Index Page"""
        return render(request, self.template_name)

#Renders the Home Page
class homeView(LoginRequiredMixin, View):
    """Home Page View Class"""
    login_url='signIn'
    template_name = 'home.html'
    def get(self, request):
        """Renders the Home Page"""
        return render(request, self.template_name)


class signInView(View):
    """Sign In View Class"""
    template_name = 'signIn.html'

    def get(self, request):
        """
        Renders the Sign In Page.\n 
        If the user is already authenticated it redirects to the HomePage.
        """
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        """
        The username and password for a user is received as a post request and 
        and the user is then logged in.\n 
        If the user cannot be logged in an error message is displayed.
        """
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
        """Logs out the current signed in user"""
        logout(request)
        return redirect('signIn')


#user registration page 
class signUpView(View):
    """Sign Up View Class"""
    template_name = 'signUp.html'
    form = CreateUserForm()
    context = {'form': form}

    def get(self, request):
        """
        Renders the Sign Up Page. If the user is already authenticated 
        it redirects to the HomePage.
        """
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        """ 
        The username, email and password for a user is received as a post request 
        and the user is then validated.\n 
        If the form is valid, a new user is created. Then, it redirects to the 
        sign in page.\n
        If the form is invalid, the sign up page is displayed.
        """
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
    """Crags View Class"""
    login_url='signIn'
    template_name = 'Crags.html'
    def get(self, request):
        """Renders the My Crags Page"""
        return render(request, self.template_name)

class myClimbsView(LoginRequiredMixin, View):
    """My Climbs View Class"""
    login_url='signIn'
    template_name = 'MyClimbs.html'
    def get(self, request):
        """
        Renders the My Climbs Page.\n
        The level of the user is passed to the frontend.
        """
        return render(request, self.template_name, {'level': userProfile.objects.get(userID=request.user).level})

class myCommunityView(LoginRequiredMixin, View):
    """MyCommunity View Class"""
    login_url='signIn'
    template_name = 'MyCommunity.html'

    def get(self, request):
        """
        Renders the MyCommunity Page.\n
        Gets all the post objects in descending chronological order.\n 
        The objects are then paginated and passed to the frontend.
        """
        posts = MBPost.objects.all().order_by('-time')
        posts_paginator = Paginator(posts, 5)
        page_no = request.GET.get('page')
        posts = posts_paginator.get_page(page_no)
        args = {'posts':posts}
        return render(request,self.template_name, args)
    
    def post(self, request):
        """
        The message and the title is received as a POST request.\n
        The time of the message is then recorded and saved to the database.
        """
        message = request.POST.get("message")
        title = request.POST.get("title")
        time = datetime.datetime.now()
        MBPost.objects.create(text=message, title=title, time=time, FKUserProfile=userProfile.objects.get(userID=request.user))
        return self.get(request)

class likePostView(LoginRequiredMixin, View):
    """Like Post View Class"""
    def get(self, request):
        """
        The post id is received as a get request.\n
        The like status of the post retrieved from the database.\n
        If the like status does not exist, then a new Like Status row
        is created in the database with a True value.\n
        If the like status object exists in the database, the value of the
        like status is inverted.\n
        The function then redirects to the My Community page.
        """
        post = MBPost.objects.get(id=request.GET.get("id"))
        try:
            postLikeStatus = MBPostLikeStatus.objects.get(
                FKUserProfile = userProfile.objects.get(userID=request.user), 
                FKMBPost = post
            )
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
    """Settings View Class"""
    login_url='signIn'
    template_name = 'Settings.html'
    def get(self, request):
        """Renders the settings view"""
        return render(request, self.template_name)

def Crags(request):
    """Renders the Crags page"""
    return render(request,'Crags.html')
class Crags1(LoginRequiredMixin, View):
    """Crags 1 View Class"""
    login_url='signIn'
    template_name = 'Crags1.html'


    def get(self, request):
        """
        Renders the Crags1 page\n
        Displays the real time weather update and potential hazard warnings\n
        """
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
    """Crags 2 View Class"""
    login_url='signIn'
    template_name = 'Crags2.html'
    def get(self, request):
        """
        Renders the Crags2 page if the specified values are not received\n
        If the Rating, Grade and Rope Length value is received as a GET request,
        the function retrieves the objects based on the three parameters.\n
        The objects are then parsed into JSON and passed as arguments for 
        rendering the Crags3 page. 
        """
        if all(x in request.GET for x in ['Rating', 'Grade', 'Rope Length']):
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
    """Crags 3 View Class"""
    login_url='signIn'
    template_name = 'Crags3.html'
    def get(self, request):
        """Renders the Crags3 page"""
        return render(request, self.template_name)

def Crags4(request):
    """Renders the Crags4 page"""
    return render(request,'Crags4.html')

class Crags5(LoginRequiredMixin, View):
    """Crags 5 View Class"""
    login_url='signIn'
    template_name = 'Crags5.html'
    def get(self, request):
        """
        Renders the Crags5 page if the specified values are not passed.\n
        If the Grade and Rating is passed as a GET request, it increases
        the level of the user by using the formula:\n
        \tln(grade*rating)\n
        The level of the user is then updated to the database.\n
        The function then redirects to the MyClimbs page.
        """
        if all(x in request.GET for x in ['Rating', 'Grade']):
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
    """Renders the Saved Crag page"""
    return render(request,'savedCrags.html')
###########################################################
