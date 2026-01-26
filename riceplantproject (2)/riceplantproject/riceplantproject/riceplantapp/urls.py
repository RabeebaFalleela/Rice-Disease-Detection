"""riceplantproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('updateprofile/',views.updateprofile,name='updateprofile'),
    path('pro/',views.pro_update,name='pro_update'),
    path('adlog/',views.adlog,name='adlog'),
    path('adhome/',views.adhome,name='adhome'),
    path('feedback/',views.feedback,name='feedback'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout,name='logout'),
    path('contact/',views.contact,name='contact'),
    path('service/',views.service,name='service'),
    path('team/',views.team,name='team'),
    path('user/',views.user,name='user'),
    path('adfeedback/',views.adfeedback,name='adfeedback'),
    path('userremove/<int:id>/',views.userremove,name='userremove'),
    path('feedremove/<int:id>/',views.feedremove,name='feedremove'),
    path('process_image/',views.process_image,name='process_image'),
    # path('uploadimage/',views.uploadimage,name='uploadimage'),


]
     