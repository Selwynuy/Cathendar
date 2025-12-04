from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.calendar_view, name='calendar'),
    path('month/<int:year>/<int:month>/', views.calendar_month, name='calendar_month'),
]

# Also handle /accounts/login/ redirects
urlpatterns += [
    path('accounts/login/', views.login_view, name='accounts_login'),
]

