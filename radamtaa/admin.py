from django.contrib import admin
from .models import Location, Mtaa, Posts, Profile

# Register your models here.

admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(Mtaa)
admin.site.register(Posts)
