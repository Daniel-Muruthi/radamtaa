from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views

urlpatterns = [
    path('landing/', views.LandingView.as_view() , name="landing"),
    ]