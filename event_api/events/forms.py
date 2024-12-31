from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EventFeedback


class EventFeedbackForm(forms.ModelForm):
    """
    Form to collect feedback for events.
    Includes a comment field and a rating field with customized widgets.
    """
    class Meta:
        model = EventFeedback
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your feedback here...'
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'placeholder': 'Rate the event (1-5)'
            }),
        }


class EventRegistrationForm(forms.Form):
    """
    Simple form to handle event registration.
    The event_id is passed as a hidden input field.
    """
    event_id = forms.IntegerField(widget=forms.HiddenInput())


class UserCreationFormCustom(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm to include an email field.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserRegistrationForm(forms.ModelForm):
    """
    Custom user registration form that includes password confirmation.
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        """
        Validates that the two password fields match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
   