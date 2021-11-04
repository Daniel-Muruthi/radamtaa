from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landingview , name="landing"),
    path('profile/', views.MyProfile.as_view() , name="profile"),
    path('home/', views.userhome , name="index"),
    path ('profile/update/', views.EditProfile, name="update"),
    path('project/<int:pk>/', views.FindMtaaView.as_view(), name='findpost'),
    path('project/<int:pk>/addcomment/', views.CommentPost, name='addcomment'),
    path('addmtaa/', views.mtaaview, name="addmtaa"),
    ]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)