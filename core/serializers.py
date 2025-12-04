from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Calendar, Event, Availability, Friend, CalendarShare, Holiday


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class CalendarSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='owner',
        write_only=True,
        required=False
    )

    class Meta:
        model = Calendar
        fields = ['id', 'owner', 'owner_id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class EventSerializer(serializers.ModelSerializer):
    calendar_name = serializers.CharField(source='calendar.name', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'calendar', 'calendar_name', 'title', 'description', 'start_time', 'end_time', 'created_at']
        read_only_fields = ['id', 'created_at']


class AvailabilitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    calendar_name = serializers.CharField(source='calendar.name', read_only=True)

    class Meta:
        model = Availability
        fields = ['id', 'user', 'calendar', 'calendar_name', 'start_time', 'end_time', 'is_busy', 'title', 'description']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FriendSerializer(serializers.ModelSerializer):
    friend = UserSerializer(read_only=True)
    friend_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='friend',
        write_only=True
    )

    class Meta:
        model = Friend
        fields = ['id', 'friend', 'friend_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CalendarShareSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    calendar_name = serializers.CharField(source='calendar.name', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = CalendarShare
        fields = ['id', 'calendar', 'calendar_name', 'user', 'user_id', 'permission']
        read_only_fields = ['id']


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['id', 'date', 'name', 'country', 'description', 'is_national']
        read_only_fields = ['id']

