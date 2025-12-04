from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('calendar_app:calendar')
    return render(request, 'calendar_app/login.html')


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('calendar_app:login')


@login_required
def calendar_view(request):
    """Main calendar view"""
    return render(request, 'calendar_app/calendar.html')


@login_required
def calendar_month(request, year=None, month=None):
    """Calendar month view"""
    return render(request, 'calendar_app/calendar.html', {
        'year': year,
        'month': month,
    })

