# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # path('', views.PostListView.as_view(), name='post_list'), # Endi 'home' orqali asosiy urls.py da
    path('post/new/', views.PostCreateView.as_view(), name='post_create'), # Yangi post yaratish
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), # Batafsil ko'rish
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'), # Tahrirlash
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'), # O'chirish
    # path('recommended/', views.RecommendedPostListView.as_view(), name='recommended_posts'), # Agar kerak bo'lsa
]