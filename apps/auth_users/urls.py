from django.urls import path
from apps.auth_users import views 

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/tahrirlash/', views.ProfileEditView.as_view(), name='edit_profile'),
]
