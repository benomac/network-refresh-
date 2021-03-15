from django.contrib import admin

from .models import UserPosts, Following
# Register your models here.

admin.site.register(UserPosts)
admin.site.register(Following)