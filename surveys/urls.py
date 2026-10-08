from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='surveys/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='surveys/logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('add-mpesa-number/', views.add_mpesa_number, name='add_mpesa_number'),
    path('surveys/', views.surveys_list, name='surveys_list'),
    path('surveys/take/<str:survey_title>/', views.take_survey, name='take_survey'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('subscriptions/pay/', views.subscription_payment, name='subscription_payment'),
    path('withdraw/', views.withdraw_funds, name='withdraw_funds'),
    path('change-password/', views.change_password, name='change_password'),
] 