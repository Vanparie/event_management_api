"""
URL configuration for event_api project.

The `urlpatterns` list routes URLs to views. For more information, please see:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from events.views import EventViewSet

# Set up a router for the API
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token endpoint
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh endpoint
    path('api/', include(router.urls)),  # API endpoints from the router
    path('', include('events.urls')),  # Include event app URLs
]

