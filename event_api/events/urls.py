from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Event-related routes
    path('', views.event_list, name='event_list'),  # Default homepage (event list)
    path('events/', views.event_list, name='event_list'),  # Event list
    path('events/<int:pk>/', views.event_detail, name='event_detail'),  # Event details
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),  # Create event
    path('events/<int:pk>/edit/', views.event_form, name='event_edit'),  # Edit event
    path('event_register/<int:event_id>/', views.event_register, name='event_register'),  # Register for event
    path('event/<int:event_id>/feedback/', views.event_feedback, name='event_feedback'),

    # Authentication-related routes
    path('signup/', views.signup, name='signup'),  # User signup
    path('register/<int:event_id>/', views.register, name='register'),  # Register for event after login
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),  # Login
    path('logout/', views.logout_view, name='logout'),  # Logout
    path('profile/', views.profile, name='profile'),  # User profile

    # User registration
    path('user_register/<int:event_id>/', views.user_register, name='user_register'),
]



