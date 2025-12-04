from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User, Calendar, Event, Availability, Friend, CalendarShare
from .serializers import (
    UserSerializer, UserRegistrationSerializer, CalendarSerializer,
    EventSerializer, AvailabilitySerializer, FriendSerializer, CalendarShareSerializer
)


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create Django session for @login_required decorator
            from django.contrib.auth import login
            login(request, user)
            
            # Also return JWT tokens for API calls
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user:
                # Create Django session for @login_required decorator
                from django.contrib.auth import login
                login(request, user)
                
                # Also return JWT tokens for API calls
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CalendarViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarSerializer

    def get_queryset(self):
        user = self.request.user
        # Return calendars owned by user or shared with user
        return Calendar.objects.filter(
            Q(owner=user) | Q(shares__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def shared_with(self, request, pk=None):
        calendar = self.get_object()
        shares = CalendarShare.objects.filter(calendar=calendar)
        serializer = CalendarShareSerializer(shares, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        # Only calendar owner can delete the calendar
        if instance.owner != self.request.user:
            raise permissions.PermissionDenied("Only the calendar owner can delete this calendar")
        instance.delete()

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        calendar = self.get_object()
        if calendar.owner != request.user:
            return Response({'error': 'Only calendar owner can share'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        permission = request.data.get('permission', CalendarShare.Permission.VIEW_ONLY)
        
        user = get_object_or_404(User, id=user_id)
        share, created = CalendarShare.objects.get_or_create(
            calendar=calendar,
            user=user,
            defaults={'permission': permission}
        )
        if not created:
            share.permission = permission
            share.save()
        
        serializer = CalendarShareSerializer(share)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        calendar_id = self.request.query_params.get('calendar_id')
        if calendar_id:
            return Event.objects.filter(calendar_id=calendar_id)
        return Event.objects.all()

    def perform_create(self, serializer):
        calendar_id = self.request.data.get('calendar')
        calendar = get_object_or_404(Calendar, id=calendar_id)
        # Check permissions
        if calendar.owner != self.request.user:
            share = CalendarShare.objects.filter(
                calendar=calendar,
                user=self.request.user,
                permission__in=[CalendarShare.Permission.EDIT, CalendarShare.Permission.ADMIN]
            ).first()
            if not share:
                raise permissions.PermissionDenied("You don't have permission to add events to this calendar")
        serializer.save()

    def perform_destroy(self, instance):
        calendar = instance.calendar
        # Check if user owns the calendar or has edit/admin permission
        if calendar.owner != self.request.user:
            share = CalendarShare.objects.filter(
                calendar=calendar,
                user=self.request.user,
                permission__in=[CalendarShare.Permission.EDIT, CalendarShare.Permission.ADMIN]
            ).first()
            if not share:
                raise permissions.PermissionDenied("You don't have permission to delete events from this calendar")
        instance.delete()


class AvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = AvailabilitySerializer

    def get_queryset(self):
        calendar_id = self.request.query_params.get('calendar_id')
        queryset = Availability.objects.all()
        if calendar_id:
            queryset = queryset.filter(calendar_id=calendar_id)
        return queryset

    def perform_create(self, serializer):
        calendar_id = self.request.data.get('calendar')
        calendar = get_object_or_404(Calendar, id=calendar_id)
        # Check if user has access to calendar
        if calendar.owner != self.request.user:
            share = CalendarShare.objects.filter(
                calendar=calendar,
                user=self.request.user
            ).first()
            if not share:
                raise permissions.PermissionDenied("You don't have access to this calendar")
        
        # Get the date range for the availability
        start_time = serializer.validated_data.get('start_time')
        end_time = serializer.validated_data.get('end_time')
        
        # Delete any existing availability for this user/calendar/date combination
        # We'll match by date (ignoring time) to ensure only one status per day
        if start_time:
            start_date = start_time.date()
            end_date = end_time.date() if end_time else start_date
            
            # Delete existing availabilities that overlap with this date range
            Availability.objects.filter(
                user=self.request.user,
                calendar=calendar,
                start_time__date__gte=start_date,
                start_time__date__lte=end_date
            ).delete()
        
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def aggregated(self, request):
        calendar_id = request.query_params.get('calendar_id')
        if not calendar_id:
            return Response({'error': 'calendar_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        calendar = get_object_or_404(Calendar, id=calendar_id)
        # Get all availabilities for this calendar
        availabilities = Availability.objects.filter(calendar=calendar)
        serializer = self.get_serializer(availabilities, many=True)
        return Response(serializer.data)


class FriendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def request(self, request):
        friend_id = request.data.get('friend_id')
        if not friend_id:
            return Response({'error': 'friend_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        friend = get_object_or_404(User, id=friend_id)
        if friend == request.user:
            return Response({'error': 'Cannot add yourself as friend'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        friend_obj, created = Friend.objects.get_or_create(
            user=request.user,
            friend=friend
        )
        serializer = self.get_serializer(friend_obj)
        return Response(serializer.data, 
                      status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class CalendarShareViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarShareSerializer

    def get_queryset(self):
        return CalendarShare.objects.filter(calendar__owner=self.request.user)
