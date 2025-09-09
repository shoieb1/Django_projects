from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login.html', views.login_page, name='login_page'),
    path('main.html', views.main_page, name='main_page'),
    path('forgot-password.html', views.forgot_password_page, name='forgot_password_page'),
    path('reset-password.html', views.reset_password_page, name='reset_password_page'),
    path('register/', views.register, name='register'),
    path('save-strength/', views.save_strength, name='save_strength'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout/', views.logout, name='logout'),
]