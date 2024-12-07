from django.contrib import admin
from django.contrib.auth.models import User  # Django's built-in User model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin  # Default admin for User model
from .models import Movies, User_details  # Import your custom models


class UserPro(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'first_name', 'last_name', 'email')


class UserDetailsPro(admin.ModelAdmin):
    list_display = ('user_id', 'contact_no')

    def get_username(self, obj):
        return obj.user_id.id
    get_username.short_description = 'id'


class MoviesPro(admin.ModelAdmin):
    list_display = ('id', 'movie', 'type', 'duration', 'image', 'rating')


# Fix: Unregister the default User admin before registering your custom admin
admin.site.unregister(User)  # Unregister default User admin
admin.site.register(User, UserPro)  # Register with your custom admin class

# Register your other models
admin.site.register(Movies, MoviesPro)
admin.site.register(User_details, UserDetailsPro)  # Ensure this model is imported and defined properly
