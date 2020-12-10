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

    # Password resets.
    path('request_password_reset/', views.request_password_reset,
            name='request_password_reset'),
    path('send_password_reset/<int:user_id>/', views.send_password_reset,
            name='send_password_reset'),
    path('password_reset_sent/', views.password_reset_sent,
            name='password_reset_sent'),
]
