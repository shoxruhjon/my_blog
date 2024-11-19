from django.contrib import admin
from .models import Post, Comment


admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_approved')  # Is_approved maydonini ko'rsatish
    list_filter = ('is_approved', 'created_at')  # Tasdiqlash holati bo‘yicha filtr

admin.site.register(Post, PostAdmin)