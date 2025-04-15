from django.contrib import admin
from .models import Post, Comment


admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_approved') 
    list_filter = ('is_approved', 'created_at') 

admin.site.register(Post, PostAdmin)