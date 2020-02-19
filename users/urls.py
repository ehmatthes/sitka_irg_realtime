"""Defines URL patterns for users"""

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    # DEV: Disabling this for now; this is not for public use yet.
    # path('register/', views.register, name='register'),
]
