from django.contrib import admin
from .models import User, Calendar, Event, Availability, Friend, CalendarShare, Holiday


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_filter = ['date_joined', 'is_staff', 'is_superuser']


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'calendar', 'start_time', 'end_time']
    search_fields = ['title', 'description']
    list_filter = ['start_time', 'calendar']


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['user', 'calendar', 'start_time', 'end_time', 'is_busy', 'title']
    list_filter = ['is_busy', 'calendar', 'start_time']
    search_fields = ['title', 'description', 'user__email', 'user__username']


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend', 'created_at']
    list_filter = ['created_at']


@admin.register(CalendarShare)
class CalendarShareAdmin(admin.ModelAdmin):
    list_display = ['calendar', 'user', 'permission']
    list_filter = ['permission', 'calendar']


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'country', 'is_national']
    search_fields = ['name', 'description']
    list_filter = ['country', 'is_national', 'date']
    date_hierarchy = 'date'
