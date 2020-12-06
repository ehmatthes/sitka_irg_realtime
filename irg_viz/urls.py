"""Defines URL patterns for irg_viz."""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'irg_viz'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
]

# View images locally.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                                    document_root=settings.MEDIA_ROOT)