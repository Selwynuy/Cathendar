from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Calendar(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calendars')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Availability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availabilities')
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='availabilities')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_busy = models.BooleanField(default=True)
    title = models.CharField(max_length=200, blank=True, help_text="Optional title/note for this availability")
    description = models.TextField(blank=True, help_text="Optional description/notes")

    class Meta:
        verbose_name_plural = 'Availabilities'

class Friend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

class CalendarShare(models.Model):
    class Permission(models.TextChoices):
        VIEW_ONLY = 'view_only', 'View Only'
        EDIT = 'edit', 'Edit'
        ADMIN = 'admin', 'Admin'

    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calendar_shares')
    permission = models.CharField(max_length=20, choices=Permission.choices, default=Permission.VIEW_ONLY)

    class Meta:
        unique_together = ('calendar', 'user')


class Holiday(models.Model):
    """Public holidays that can be displayed in calendars"""
    date = models.DateField()
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=10, help_text="ISO country code (e.g., 'US', 'GB', 'CA')")
    description = models.TextField(blank=True)
    is_national = models.BooleanField(default=True, help_text="Whether this is a national holiday")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('date', 'name', 'country')
        ordering = ['date']
        indexes = [
            models.Index(fields=['date', 'country']),
        ]

    def __str__(self):
        return f"{self.name} ({self.date})"
