from rest_framework import serializers
from .models import Event, EventFeedback, RecurringEvent, Notification

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')

    class Meta:
        model = Event
        fields = '__all__'


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'capacity', 'registered_users']

    def validate(self, data):
        """Ensure event capacity is not exceeded."""
        event = self.instance
        if event.is_full():
            raise serializers.ValidationError("This event is fully booked.")
        return data
    

class EventFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFeedback
        fields = ['id', 'event', 'user', 'feedback_text', 'created_at']
        read_only_fields = ['id', 'event', 'user', 'created_at']    


class RecurringEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringEvent
        fields = ['id', 'event', 'recurrence_pattern', 'start_date', 'end_date', 'frequency']
        read_only_fields = ['id']  # Making the ID read-only        


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'event', 'message', 'created_at', 'read', 'notify_at']
        read_only_fields = ['id', 'created_at']        