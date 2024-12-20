from django.shortcuts import render

from rest_framework import viewsets, permissions, generics
from .models import Event, EventFeedback, RecurringEvent, Notification
from .serializers import EventSerializer
from django.utils import timezone
from rest_framework import filters
from rest_framework.filters import SearchFilter

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import EventRegistrationSerializer, EventFeedbackSerializer, RecurringEventSerializer, NotificationSerializer

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

import icalendar
from django.http import HttpResponse

from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import EventFeedbackForm, EventForm


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]   # Only authenticated users can perform actions
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title', 'location']

    def perform_create(self, serializer):
        # Ensure that the organizer is the current authenticated user
        serializer.save(organizer=self.request.user)

    def update(self, request, *args, **kwargs):
        # Ensure the user can only edit their own events
        event = self.get_object()
        if event.organizer != request.user:
            return Response({'detail': 'You cannot edit this event.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def get_queryset(self):
        # ensures only future/upcoming events are shown
        return Event.objects.filter(date_time__gte=timezone.now())


# endpoint for event registration
class RegisterForEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        if event.is_full():
            return Response({"error": "This event is fully booked."}, status=status.HTTP_400_BAD_REQUEST)

        event.registered_users.add(request.user)
        serializer = EventRegistrationSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)    


# Allow filtering by category
class EventListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


# Generate calendar URLs
def generate_icalendar(request, event_id):
    event = Event.objects.get(id=event_id)
    cal = icalendar.Calendar()
    event_item = icalendar.Event()
    event_item.add('summary', event.title)
    event_item.add('dtstart', event.date_time)
    event_item.add('location', event.location)
    cal.add_component(event_item)

    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="{event.title}.ics"'
    return response    


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()  # Queryset to retrieve the event data
    serializer_class = EventSerializer  # Serializer class to format the event data
    lookup_field = 'pk'  # This will use the primary key (pk) in the URL to identify the event


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventSearchView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['title', 'description', 'category']        


class EventFeedbackListView(generics.ListCreateAPIView):
    serializer_class = EventFeedbackSerializer

    def get_queryset(self):
        """
        This view returns a list of feedback for a specific event.
        """
        event_id = self.kwargs['event_id']
        return EventFeedback.objects.filter(event_id=event_id)  # Filter feedback by event      
    

class RecurringEventView(generics.CreateAPIView):
    queryset = RecurringEvent.objects.all()
    serializer_class = RecurringEventSerializer  

class RecurringEventListView(generics.ListCreateAPIView):
    queryset = RecurringEvent.objects.all()
    serializer_class = RecurringEventSerializer

class RecurringEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecurringEvent.objects.all()
    serializer_class = RecurringEventSerializer      


class NotificationListView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer    


class CalendarIntegrationView(APIView):
    def get(self, request, *args, **kwargs):
        # Example: Return events to add to a calendar
        events = Event.objects.all()
        event_data = [{"title": event.title, "date": event.date} for event in events]
        return Response(event_data)    
    

def root_view(request):
    return HttpResponse("Welcome to the Event Management API!") 


# Function-Based Views
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


# View for user registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    
    return render(request, 'events/register.html', {'form': form})


# View for user login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event_list')  # Redirect to event list after login
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})


# View for user logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout


# profile view
def profile(request):
    return render(request, 'profile.html')  # Create a template for displaying user profile


# event feedback view
@login_required
def event_feedback(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.event = event
            feedback.user = request.user
            feedback.save()
            return redirect('event_list')  # Redirect back to event list or event details page
    else:
        form = EventFeedbackForm()

    return render(request, 'events/event_feedback.html', {'form': form, 'event': event})



# Event Form View

@login_required
def event_form(request, pk=None):
    if pk:      # If pk is provided, we are editing an existing event
        event = get_object_or_404(Event, pk=pk)
    else:       # Otherwise, we are creating a new event
        event = None
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')  # Redirect after event creation/editing
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {'form': form, 'event': event})