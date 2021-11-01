from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('landing/', views.LandingView.as_view() , name="landing"),
    path('profile/', views.profile , name="profile"),
    path('', views.userhome , name="index"),
    path ('profile/update/', views.EditProfile, name="update"),
    ]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)