from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import User, Calendar, Event, Availability, Friend, CalendarShare
from .serializers import (
    UserSerializer, CalendarSerializer, EventSerializer,
    AvailabilitySerializer, FriendSerializer, CalendarShareSerializer
)


class AdminUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=30)
        ).count()
        return Response({
            'total_users': total_users,
            'active_users': active_users,
        })


class AdminCalendarViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_calendars = Calendar.objects.count()
        shared_calendars = Calendar.objects.filter(shares__isnull=False).distinct().count()
        return Response({
            'total_calendars': total_calendars,
            'shared_calendars': shared_calendars,
        })


class AdminEventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_events = Event.objects.count()
        upcoming_events = Event.objects.filter(start_time__gte=timezone.now()).count()
        return Response({
            'total_events': total_events,
            'upcoming_events': upcoming_events,
        })


class AdminAnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        # User stats
        total_users = User.objects.count()
        active_users = User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        # Calendar stats
        total_calendars = Calendar.objects.count()
        shared_calendars = Calendar.objects.filter(shares__isnull=False).distinct().count()
        
        # Event stats
        total_events = Event.objects.count()
        upcoming_events = Event.objects.filter(start_time__gte=timezone.now()).count()
        
        # Availability stats
        total_availabilities = Availability.objects.count()
        busy_markers = Availability.objects.filter(is_busy=True).count()
        
        # Friend stats
        total_friendships = Friend.objects.count()
        
        return Response({
            'users': {
                'total': total_users,
                'active': active_users,
            },
            'calendars': {
                'total': total_calendars,
                'shared': shared_calendars,
            },
            'events': {
                'total': total_events,
                'upcoming': upcoming_events,
            },
            'availability': {
                'total_markers': total_availabilities,
                'busy_markers': busy_markers,
            },
            'friendships': {
                'total': total_friendships,
            },
        })

