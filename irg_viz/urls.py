"""Defines URL patterns for irg_viz."""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'irg_viz'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Simple plot of the river gauge.
    path('simple_irg_plot', views.simple_irg_plot, name='simple_irg_plot'),

    # Interactive critical forecast plot.
    path('irg_critical_forecast_plot_interactive',
            views.irg_critical_forecast_plot_interactive,
            name='irg_critical_forecast_plot_interactive'),

    # Static critical forecast plot.
    path('irg_critical_forecast_plot', views.irg_critical_forecast_plot,
            name='irg_critical_forecast_plot'),

]

# View images locally.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                                    document_root=settings.MEDIA_ROOT)