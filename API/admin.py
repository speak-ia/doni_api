from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser

@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin', 'is_enqueteur')}),
    )
    list_display = ['username', 'email', 'is_admin', 'is_enqueteur']
