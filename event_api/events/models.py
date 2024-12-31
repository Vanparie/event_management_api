from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    """
    Represents an event with details like title, description, organizer, and capacity.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    capacity = models.PositiveIntegerField()
    registered_users = models.ManyToManyField(User, related_name='registered_events', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    CATEGORY_CHOICES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('concert', 'Concert'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')

    def is_past_due(self):
        """
        Checks if the event date and time are in the past.
        """
        return self.date_time < timezone.now()

    def is_full(self):
        """
        Checks if the event has reached its maximum capacity.
        """
        return self.registered_users.count() >= self.capacity

    def __str__(self):
        return self.title


class EventFeedback(models.Model):
    """
    Stores feedback for an event, including a comment and a rating from the user.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} for {self.event.title}"

class Feedback(models.Model):
    event = models.ForeignKey(Event, related_name="feedbacks", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="feedbacks", on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s feedback for {self.event.title}"


class RecurringEvent(models.Model):
    """
    Represents recurring patterns for an event (e.g., weekly, monthly).
    """
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    recurrence_pattern = models.CharField(
        max_length=255,
        choices=[('weekly', 'Weekly'), ('monthly', 'Monthly')]
    )
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    frequency = models.IntegerField(default=1, help_text="Frequency of recurrence (e.g., every 1 week)")

    def __str__(self):
        return f"{self.event.title} - {self.recurrence_pattern} starting {self.start_date}"


class Notification(models.Model):
    """
    Represents a notification sent to a user about an event.
    """
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    notify_at = models.DateTimeField()

    def __str__(self):
        return f"Notification for {self.user.username} about {self.event.title}"


class Registration(models.Model):
    """
    Represents a user's registration for an event.
    """
    event = models.ForeignKey(Event, related_name="registrations", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="registrations", on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"
