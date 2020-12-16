"""Defines URL patterns for irg_viz."""

from django.urls import path

from . import views
import irg_viz.views as irg_views


app_name = 'accounts'
urlpatterns = [
    # Override django-allauth logout url. It asks to confirm logout, this 
    #   is just a simple, direct logout and redirect to home page.
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # Override urls from django-allauth that I don't want available.
    #   Redirect these to index.
    path('signup/', irg_views.index),
]

