"""Defines URL patterns for irg_viz."""

from django.urls import path

from . import views

app_name = 'irg_viz'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Simple plot of the river gauge.
    path('simple_irg_plot', views.simple_irg_plot, name='simple_irg_plot'),
    # Cone plot, like a hurricane path forecast.
    path('irg_cone_plot', views.irg_cone_plot, name='irg_cone_plot'),
    # Critical forecast plot, showing projections over next ~5 hours.
    path('irg_critical_forecast_plot', views.irg_critical_forecast_plot,
            name='irg_critical_forecast_plot'),
]