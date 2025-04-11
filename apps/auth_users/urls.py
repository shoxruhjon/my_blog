# project_name/urls.py (asosiy loyiha uchun) yoki users/urls.py (ilovangiz uchun)

from django.urls import path
# Agar users ilovasida bo'lsa: from . import views
# Agar asosiy loyihada bo'lsa: from users import views (yoki ilovangiz nomi)
from apps.auth_users import views # Ilovangiz nomiga moslang

urlpatterns = [
    # path('register/', views.register_view, name='register'),
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.login_view, name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Boshqa URL manzillaringiz...
    path('', views.home_view, name='home'), # Masalan, bosh sahifa uchun
]

# Agar bu users ilovasining urls.py fayli bo'lsa,
# asosiy project_name/urls.py fayliga quyidagicha qo'shing:
# from django.urls import include
# path('users/', include('users.urls')), # yoki 'accounts/' kabi prefiks

