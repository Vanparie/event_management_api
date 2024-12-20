from django.contrib import admin
from .models import Event, EventFeedback, RecurringEvent, Notification

# Register Event model
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category', 'date_time', 'location', 'organizer', 'capacity', 'get_registered_users_count', 'created_at', 'is_full', 'is_past_due')
    search_fields = ('title', 'description', 'location', 'category', 'organizer__username')
    list_filter = ('category', 'organizer', 'date_time')
    ordering = ('date_time',)

    def get_registered_users_count(self, obj):
        """Returns the count of registered users."""
        return obj.registered_users.count()
    get_registered_users_count.short_description = 'Registered Users Count'

    def is_full(self, obj):
        """Returns whether the event is full."""
        return obj.is_full()
    is_full.boolean = True  # Show as a boolean (True/False)

    def is_past_due(self, obj):
        """Returns whether the event is in the past."""
        return obj.is_past_due()
    is_past_due.boolean = True  # Show as a boolean (True/False)


# Register EventFeedback model
@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'comment', 'rating', 'created_at')  
    search_fields = ('event__title', 'user__username', 'comment')  # Search by event title or user username
    list_filter = ('event', 'user', 'rating')  # Filter by event or user
    ordering = ('-created_at',)

# Register RecurringEvent model
@admin.register(RecurringEvent)
class RecurringEventAdmin(admin.ModelAdmin):
    list_display = ('event', 'recurrence_pattern', 'start_date', 'end_date', 'frequency')  # Correct field names
    search_fields = ('event__title', 'recurrence_pattern')  # Search by event title
    list_filter = ('recurrence_pattern', 'start_date', 'end_date')  # Filter by recurrence pattern (weekly, monthly)
    ordering = ('-start_date',)  # Order by start date

# Register Notification model
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'message', 'created_at', 'read', 'notify_at')  # Correct field names
    search_fields = ('event__title', 'user__username', 'message')  # Search by event title or user username or message
    list_filter = ('created_at', 'read', 'notify_at')  # Filter by created and notify at time and read status
    ordering = ('-notify_at', '-created_at')  # Order by scheduled notification time
