from django import forms
from .models import EventFeedback, Event

class EventFeedbackForm(forms.ModelForm):
    class Meta:
        model = EventFeedback
        fields = ['comment', 'rating']  # other fields can be added if needed, like 'user' or 'event'
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your feedback here...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'placeholder': 'Rate the event (1-5)'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_time', 'location', 'capacity', 'category']  # all needed fields can be included
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Event description'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }        