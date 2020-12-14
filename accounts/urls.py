"""Defines URL patterns for irg_viz."""

from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    # Override django-allauth logout url. It asks to confirm logout, this 
    #   is just a simple, direct logout and redirect to home page.
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile, name='profile'),
]

