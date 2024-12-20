from django.urls import path
from . import views

urlpatterns = [
    # Event List and Detail
    path('events/', views.EventListView.as_view(), name='event_list'),  # GET all events
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),  # GET, PUT, DELETE specific event

    # Create Event
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),  # POST to create a new event

    # User Registration for Events
    path('events/<int:event_id>/register/', views.RegisterForEventView.as_view(), name='register_event'),

    # Filtering and Search
    path('events/search/', views.EventSearchView.as_view(), name='event_search'),  # GET for filtered results

    # Recurring Events
    path('events/<int:event_id>/recurring/', views.RecurringEventView.as_view(), name='recurring_event'),  # GET or manage recurring event details

    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),  # GET notifications

    # Calendar Integration
    path('events/<int:event_id>/calendar/', views.CalendarIntegrationView.as_view(), name='calendar_integration'),  # Export to external calendar
    
    # Event Comments and Feedback
    path('events/<int:event_id>/feedback/', views.EventFeedbackListView.as_view(), name='event_feedback_list'),   # GET and POST comments for an event

    path('', views.event_list, name='event_list'),
    path('events-fbv/<int:pk>/', views.event_detail, name='event_detail'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('events/<int:pk>/feedback/', views.event_feedback, name='event_feedback'),
    path('events/new/', views.event_form, name='event_create'),
    path('events/<int:pk>/edit/', views.event_form, name='event_edit'),
]


