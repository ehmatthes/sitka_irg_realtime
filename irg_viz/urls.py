"""Defines URL patterns for irg_viz."""

from django.urls import path

from . import views

app_name = 'irg_viz'
urlpatterns = [
    # Home page
    path('', views.index, name='index')
]