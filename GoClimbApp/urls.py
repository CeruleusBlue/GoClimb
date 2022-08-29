from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static  

urlpatterns = [
    path('',views.index),
    path('index', views.index, name="index"),
    path('home', views.home, name="home"),
    path('signIn', views.signInView.as_view(), name="signIn"),
    path('signUp', views.signUpView.as_view(), name="signUp"),
    path('logout/', views.logoutUser, name="logout"),
    path('Crags', views.Crags, name="Crags"),
    path('MyClimbs', views.MyClimbs, name="MyClimbs"),
    path('MyCommunity', views.MyCommunity, name="MyCommunity"),
    path('MyCommunity/create', views.MyCommunityCreate, name="MyCommunityCreate" ),
    path('Settings', views.Settings, name="Settings"),

]+ static(settings.MEDIA_URL,
                   document_root=settings.MEDIA_ROOT)

#    path('',views.indexView.as_view()),
#    path('index', views.indexView.as_view(), name="index"),
#    path('home', views.homeView.as_view(), name="home"),
#    path('signIn', views.signInView.as_view(), name="signIn"),
#    path('signUp', views.signUpView.as_view(), name="signUp"),
#    path('Crags', views.cragsView.as_view(), name="Crags"),
#    path('MyClimbs', views.myClimbsView.as_view(), name="MyClimbs"),
#    path('MyCommunity', views.myCommunityView.as_view(), name="MyCommunity"),
#    path('Settings', views.settingsView.as_view(), name="Settings"),