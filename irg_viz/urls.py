"""Defines URL patterns for irg_viz."""

from django.urls import path

from . import views

app_name = 'irg_viz'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Simple plot of the river gauge.
    path('simple_irg_plot', views.simple_irg_plot, name='simple_irg_plot'),
]