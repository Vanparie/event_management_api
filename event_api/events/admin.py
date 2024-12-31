from django.contrib import admin
from .models import Event, EventFeedback, RecurringEvent, Notification

# Admin customization for Event model
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'category', 'date_time', 'location',
        'organizer', 'capacity', 'get_registered_users_count',
        'created_at', 'is_full', 'is_past_due'
    )
    search_fields = ('title', 'description', 'location', 'category', 'organizer__username')
    list_filter = ('category', 'organizer', 'date_time')
    ordering = ('date_time',)

    def get_registered_users_count(self, obj):
        """Display the count of users registered for the event."""
        return obj.registered_users.count()
    get_registered_users_count.short_description = 'Registered Users Count'

    def is_full(self, obj):
        """Indicate whether the event has reached its capacity."""
        return obj.is_full()
    is_full.boolean = True

    def is_past_due(self, obj):
        """Indicate whether the event date/time is in the past."""
        return obj.is_past_due()
    is_past_due.boolean = True


# Admin customization for EventFeedback model
@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'comment', 'rating', 'created_at')
    search_fields = ('event__title', 'user__username', 'comment')
    list_filter = ('event', 'user', 'rating')
    ordering = ('-created_at',)


# Admin customization for RecurringEvent model
@admin.register(RecurringEvent)
class RecurringEventAdmin(admin.ModelAdmin):
    list_display = ('event', 'recurrence_pattern', 'start_date', 'end_date', 'frequency')
    search_fields = ('event__title', 'recurrence_pattern')
    list_filter = ('recurrence_pattern', 'start_date', 'end_date')
    ordering = ('-start_date',)


# Admin customization for Notification model
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'message', 'created_at', 'read', 'notify_at')
    search_fields = ('event__title', 'user__username', 'message')
    list_filter = ('created_at', 'read', 'notify_at')
    ordering = ('-notify_at', '-created_at')
