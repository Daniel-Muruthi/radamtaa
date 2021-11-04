from django.contrib import admin
from .models import Comment, Location, Mtaa, Posts, Profile

# Register your models here.

admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(Mtaa)
admin.site.register(Posts)
admin.site.register(Comment)
