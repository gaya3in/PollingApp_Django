"""PollingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from Polling import views

urlpatterns = [
    path('',views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('home/', views.home_view, name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('create/', views.createpoll_view, name="create"),
    path('profile/', views.profile_view, name="profile"),
    path('vote/<int:poll_id>/',views.vote_view, name="vote"),
    path('results/<int:poll_id>/', views.results_view, name="results"),

]
