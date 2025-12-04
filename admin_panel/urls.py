from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('', views.admin_dashboard, name='dashboard'),
    path('users/', views.admin_users, name='users'),
    path('calendars/', views.admin_calendars, name='calendars'),
    path('events/', views.admin_events, name='events'),
    path('analytics/', views.admin_analytics, name='analytics'),
]

