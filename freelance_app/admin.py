from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'profile_photo', 'user_type',
            'skills', 'experience', 'portfolio_url', 'cv_file', 'location',
            'company_name', 'description', 'website'
        )}),
    )

admin.site.register(User, CustomUserAdmin)
