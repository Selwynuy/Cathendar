from rest_framework import permissions
from .models import CalendarShare


class IsCalendarOwnerOrShared(permissions.BasePermission):
    """
    Permission to check if user owns calendar or has share access.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'calendar'):
            calendar = obj.calendar
        elif hasattr(obj, 'owner'):
            calendar = obj
        else:
            return False
        
        if calendar.owner == request.user:
            return True
        
        share = CalendarShare.objects.filter(
            calendar=calendar,
            user=request.user
        ).first()
        return share is not None


class CanEditCalendar(permissions.BasePermission):
    """
    Permission to check if user can edit calendar (owner or edit/admin permission).
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'calendar'):
            calendar = obj.calendar
        elif hasattr(obj, 'owner'):
            calendar = obj
        else:
            return False
        
        if calendar.owner == request.user:
            return True
        
        share = CalendarShare.objects.filter(
            calendar=calendar,
            user=request.user,
            permission__in=[CalendarShare.Permission.EDIT, CalendarShare.Permission.ADMIN]
        ).first()
        return share is not None

