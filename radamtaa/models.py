from django.db import models
import datetime as dt
from datetime import datetime 
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.shortcuts import get_object_or_404,render,HttpResponseRedirect
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
from django.contrib import auth
from django.utils.text import slugify 
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICES = (
   ('M', 'Male'),
   ('F', 'Female'),
   ('O', 'Other')
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.CharField(null=True, max_length=255)
    phonenumber = models.IntegerField(null=True)
    bio = models.CharField(blank=True,max_length=255)
    houselocation = models.CharField(blank=True,max_length=255)
    userpic = CloudinaryField('image')
    gender = models.CharField(max_length=11, choices=GENDER_CHOICES, default='Male')

    def __str__(self):
        return self.user.username


    @classmethod
    def getProfileByName(cls, username):
        uprofile = cls.objects.filter(username=username)
        return uprofile


class Location(models.Model):
    location=models.CharField(max_length=30)

    objects = models.Manager()

    def __str__(self):
        return self.location

class Mtaa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mtaapic = CloudinaryField("image")
    name = models.CharField(max_length=150)
    residents_number= models.PositiveIntegerField(default=0)
    location = models.ForeignKey(Location)

    @classmethod
    def get_mtaa(cls):
        mitaa = Mtaa.objects.all()
        return mitaa

    class Meta:
        ordering = ['name']

    @classmethod
    def search_mtaa(cls,searchmtaa):
        mitaa = cls.objects.filter(id__icontains = searchmtaa)
        return mitaa

class Posts(models.Model):
	title = models.CharField(max_length = 300)
	mtaa = models.ForeignKey(Mtaa)
	author = models.ForeignKey(User, null=True)
	content = models.TextField()

	def __str__(self):
		return self.title
	def save_posts(self):
		self.save()

	def delete_posts(self):
		self.delete()


