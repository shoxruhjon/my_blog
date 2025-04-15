# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'created_at']
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'groups', 'created_at')

    fieldsets = UserAdmin.fieldsets + (
        ('Maxsus ma\'lumotlar', {'fields': ('bio', 'profile_picture', 'birth_date', 'location')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Maxsus ma\'lumotlar', {'fields': ('first_name', 'last_name', 'bio', 'profile_picture', 'birth_date', 'location')}),
    )

    readonly_fields = ('last_login', 'date_joined', 'created_at')

    ordering = ('-created_at',)

admin.site.register(CustomUser, CustomUserAdmin)

