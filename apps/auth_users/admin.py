# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Ro'yxatda 'created_at' ni ham ko'rsatamiz
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'created_at']
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'groups', 'created_at')  # 'created_at' bo'yicha filtr

    # Maydon guruhlarini yangilaymiz
    fieldsets = UserAdmin.fieldsets + (
        ('Maxsus ma\'lumotlar', {'fields': ('bio', 'profile_picture', 'birth_date', 'location')}),
        # 'last_login' va 'date_joined' allaqachon mavjud, shuning uchun ularni qayta kiritmaymiz
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Maxsus ma\'lumotlar', {'fields': ('first_name', 'last_name', 'bio', 'profile_picture', 'birth_date', 'location')}),
    )

    # 'created_at' maydonini faqat o'qish uchun qilamiz (avtomatik to'ldirilgani uchun)
    readonly_fields = ('last_login', 'date_joined', 'created_at')

    ordering = ('-created_at',)  # Yaratilgan vaqt bo'yicha teskari tartiblash

admin.site.register(CustomUser, CustomUserAdmin)

