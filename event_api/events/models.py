from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    capacity = models.PositiveIntegerField()
    registered_users = models.ManyToManyField(User, related_name='registered_events', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # allow filtering by category
    CATEGORY_CHOICES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('concert', 'Concert'),
    ]
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')


    def is_past_due(self):
        return self.date_time < timezone.now()
    
    def is_full(self):
        """Check if the event is fully booked."""
        return self.registered_users.count() >= self.capacity
    
    def __str__(self):
        return self.title


# Add a feedback model and API for comments

class EventFeedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class RecurringEvent(models.Model):
    """
    Model to store recurring event details.
    """
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    recurrence_pattern = models.CharField(
        max_length=255, 
        choices=[
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly')
        ]
    )  # Defines how the event recurs (e.g., weekly or monthly)

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    frequency = models.IntegerField(default=1)  # E.g., every 1 week, every 2 weeks, etc.

    def __str__(self):
        return f"{self.event.title} - {self.recurrence_pattern} starting {self.start_date}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    notify_at = models.DateTimeField()

    def __str__(self):
        return f"Notification for {self.user.username} about {self.event.title}"    
