from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView, UserLoginView, UserViewSet,
    CalendarViewSet, EventViewSet, AvailabilityViewSet,
    FriendViewSet, CalendarShareViewSet
)
from .admin_views import (
    AdminUserViewSet, AdminCalendarViewSet, AdminEventViewSet, AdminAnalyticsViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'calendars', CalendarViewSet, basename='calendar')
router.register(r'events', EventViewSet, basename='event')
router.register(r'availability', AvailabilityViewSet, basename='availability')
router.register(r'friends', FriendViewSet, basename='friend')
router.register(r'calendar-shares', CalendarShareViewSet, basename='calendar-share')

# Admin panel routes
admin_router = DefaultRouter()
admin_router.register(r'users', AdminUserViewSet, basename='admin-user')
admin_router.register(r'calendars', AdminCalendarViewSet, basename='admin-calendar')
admin_router.register(r'events', AdminEventViewSet, basename='admin-event')
admin_router.register(r'analytics', AdminAnalyticsViewSet, basename='admin-analytics')

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', include(admin_router.urls)),
    path('', include(router.urls)),
]

