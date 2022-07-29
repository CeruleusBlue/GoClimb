from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static  

urlpatterns = [
    path('',views.index),
    path('index', views.index, name="index"),
    path('home', views.home, name="home"),
    path('signIn', views.signIn, name="signIn"),
    path('signUp', views.signUp, name="signUp"),
    path('Crags', views.Crags, name="Crags"),
    path('MyClimbs', views.MyClimbs, name="MyClimbs"),
    path('MyCommunity', views.MyCommunity, name="MyCommunity"),
    path('Settings', views.Settings, name="Settings"),

]+ static(settings.MEDIA_URL,
                   document_root=settings.MEDIA_ROOT)
