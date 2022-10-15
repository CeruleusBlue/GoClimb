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
    ######################################################
    path('Crags1', views.Crags1.as_view(), name="Crags1"),
    path('Crags2', views.Crags2.as_view(), name="Crags2"),
    path('Crags3', views.Crags3.as_view(), name="Crags3"),
    path('Crags4', views.Crags4, name="Crags4"),
    path('Crags5', views.Crags5.as_view(), name="Crags5"),
    #######################################################
    path('MyClimbs/', views.myClimbsView.as_view(), name="MyClimbs"),
    path('MyCommunity', views.myCommunityView.as_view(), name="MyCommunity"),
    path('likePost', views.likePostView.as_view(),name="likePost"),
    path('Settings', views.settingsView.as_view(), name="Settings"),
    path('logout/', views.logoutUser, name="logout"),



]+ static(settings.MEDIA_URL,
                   document_root=settings.MEDIA_ROOT)
