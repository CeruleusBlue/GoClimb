from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static  

urlpatterns = [
    path('',views.indexView.as_view()),
    path('index', views.indexView.as_view(), name="index"),
    path('home', views.homeView.as_view(), name="home"),
    path('signIn', views.signInView.as_view(), name="signIn"),
    path('signUp', views.signUpView.as_view(), name="signUp"),
    path('Crags', views.cragsView.as_view(), name="Crags"),
    path('MyClimbs', views.myClimbsView.as_view(), name="MyClimbs"),
    path('MyCommunity', views.myCommunityView.as_view(), name="MyCommunity"),
    path('Settings', views.settingsView.as_view(), name="Settings"),
    path('logout/', views.logoutUser, name="logout"),
    #path('', views.route, name="route"),
	  path('map', views.map, name="map"),



]+ static(settings.MEDIA_URL,
                   document_root=settings.MEDIA_ROOT)