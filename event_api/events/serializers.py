from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, EventFeedback, RecurringEvent, Notification


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model, exposing all fields with a readable organizer field.
    """
    organizer = serializers.ReadOnlyField(source='organizer.username')

    class Meta:
        model = Event
        fields = '__all__'


class EventRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for event registration, ensuring capacity constraints.
    """
    class Meta:
        model = Event
        fields = ['id', 'title', 'capacity', 'registered_users']

    def validate(self, data):
        """
        Validate that the event has not exceeded its capacity.
        """
        event = self.instance
        if event.is_full():
            raise serializers.ValidationError("This event is fully booked.")
        return data


class EventFeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for EventFeedback model, exposing relevant fields.
    """
    class Meta:
        model = EventFeedback
        fields = ['id', 'event', 'user', 'comment', 'rating', 'created_at']
        read_only_fields = ['id', 'event', 'user', 'created_at']


class RecurringEventSerializer(serializers.ModelSerializer):
    """
    Serializer for RecurringEvent model, managing recurrence-related data.
    """
    class Meta:
        model = RecurringEvent
        fields = ['id', 'event', 'recurrence_pattern', 'start_date', 'end_date', 'frequency']
        read_only_fields = ['id']  # Prevents updates to the primary key


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model, managing user notifications.
    """
    class Meta:
        model = Notification
        fields = ['id', 'user', 'event', 'message', 'created_at', 'read', 'notify_at']
        read_only_fields = ['id', 'created_at']


class RegistrationSerializer(serializers.Serializer):
    """
    Custom serializer for user registration, ensuring password validation.
    """
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Ensure passwords match during user registration.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Create a new user with the validated registration data.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
      