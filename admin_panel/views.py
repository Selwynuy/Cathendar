from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import json


def admin_login(request):
    """Custom admin panel login page"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user and user.is_staff:
                login(request, user)
                return redirect('admin_panel:dashboard')
            else:
                messages.error(request, 'Invalid credentials or you are not a staff member.')
    
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    """Custom admin panel logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_panel:login')


@staff_member_required
def admin_dashboard(request):
    """Main admin panel dashboard"""
    return render(request, 'admin_panel/dashboard.html')


@staff_member_required
def admin_users(request):
    """Users management page"""
    return render(request, 'admin_panel/users.html')


@staff_member_required
def admin_calendars(request):
    """Calendars management page"""
    return render(request, 'admin_panel/calendars.html')


@staff_member_required
def admin_events(request):
    """Events management page"""
    return render(request, 'admin_panel/events.html')


@staff_member_required
def admin_analytics(request):
    """Analytics dashboard"""
    return render(request, 'admin_panel/analytics.html')
