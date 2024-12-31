from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Event, Registration, Feedback
from .forms import UserRegistrationForm, EventFeedbackForm
from .serializers import EventSerializer, RegistrationSerializer


# DRF ViewSet for Event
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=['post'], url_path='register')
    def register_user(self, request, pk=None):
        """Custom action to register a user for an event via API."""
        event = get_object_or_404(Event, pk=pk)
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            password2 = serializer.validated_data['password2']

            if password != password2:
                return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, email=email, password=password)

            if event.is_full():
                return Response({"error": "Event is at full capacity."}, status=status.HTTP_400_BAD_REQUEST)

            event.registered_users.add(user)
            event.save()
            return Response({"success": f"User '{username}' registered successfully for '{event.title}'."},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Function-Based Views
def event_list(request):
    """List all upcoming events."""
    events = Event.objects.filter(date_time__gte=timezone.now()).order_by('date_time')
    return render(request, 'events/event_list.html', {'events': events})


@login_required
def event_detail(request, pk):
    """View details of a specific event."""
    event = get_object_or_404(Event, pk=pk)
    user_registered = event.registrations.filter(user=request.user).exists()
    is_past_due = event.is_past_due()

    if request.method == 'POST':
        feedback_form = EventFeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.event = event
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Your feedback has been submitted.")
            return redirect('event_detail', pk=pk)
    else:
        feedback_form = EventFeedbackForm()

    return render(request, 'events/event_detail.html', {
        'event': event,
        'feedback_form': feedback_form,
        'user_registered': user_registered,
        'is_past_due': is_past_due,
    })


def event_register(request, event_id):
    """Register a user for an event."""
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'events/event_register.html', {'event_id': event_id})

        user = User.objects.create_user(username=username, email=email, password=password)

        Registration.objects.create(user=user, event=event)

        messages.success(request, "You have successfully registered for the event.")
        return redirect('event_detail', pk=event.id)

    return render(request, 'events/event_register.html', {'event_id': event_id})


def user_register(request, event_id):
    """User registration and event registration."""
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            event.registered_users.add(user)
            messages.success(request, "You have successfully registered for the event!")
            return redirect('event_detail', pk=event.pk)
        else:
            messages.error(request, "Registration failed. Please check your details and try again.")
    else:
        form = UserRegistrationForm()

    return render(request, 'events/user_register.html', {'form': form, 'event': event})


def register(request, event_id):
    """User signup and event registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_register', event_id=event_id)
    else:
        form = UserRegistrationForm()

    return render(request, 'events/register.html', {'form': form, 'event_id': event_id})


def signup(request):
    """Handle user sign-up."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully. Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    """Log the user out."""
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect('event_list')
    return render(request, 'events/logout.html')


# Generic Views
class EventCreateView(CreateView):
    """Create a new event."""
    model = Event
    fields = ['title', 'description', 'date_time', 'location', 'capacity']
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')


def event_form(request, pk):
    """Edit an event."""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
         # Extract data from the form submission
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_time = request.POST.get('date_time')
        location = request.POST.get('location')
        category = request.POST.get('category')
        capacity = request.POST.get('capacity')

        if event:  # Editing an existing event
            event.title = title
            event.description = description
            event.date_time = date_time
            event.location = location
            event.category = category
            event.capacity = capacity
            event.save()
            messages.success(request, 'Event updated successfully!')
        else:  # Creating a new event
            event = Event.objects.create(
                title=title,
                description=description,
                date_time=date_time,
                location=location,
                category=category,
                capacity=capacity,
            )
            messages.success(request, 'Event created successfully!')

        return redirect('event_list')  # Redirect to the event list page

    # Render the form template with the existing event data or a blank form
    return render(request, 'events/eventform.html', {'event': event})


def profile(request):
    """User profile page."""
    return render(request, 'events/profile.html')


def event_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    feedbacks = event.feedbacks.all()  # Get all feedbacks for the event

    # Handle the feedback submission
    if request.method == "POST":
        comment = request.POST.get("comment")
        rating = request.POST.get("rating")

        # Create feedback entry
        Feedback.objects.create(
            event=event,
            user=request.user,
            comment=comment,
            rating=rating,
        )
        return redirect('event_feedback', event_id=event.id)

    return render(request, 'events/event_feedback.html', {
        'event': event,
        'feedbacks': feedbacks
    })
