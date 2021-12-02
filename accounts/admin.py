from django.contrib import admin

from .models import Profile, FriendRequest

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'photo']
    list_filter = ['city']


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'timestamp']
    list_filter = ['from_user', 'to_user', 'timestamp']
