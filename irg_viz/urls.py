"""Defines URL patterns for irg_viz."""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'irg_viz'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # About pages
    path('about/', views.about, name='about'),
    path('hist_examples/', views.hist_examples, name='hist_examples'),

    # Working with notifications (site admins only).
    path('new_notification/', views.new_notification, name='new_notification'),
    path('edit_notification/<int:notification_id>/', views.edit_notification,
            name='edit_notification'),
    path('all_notifications/', views.all_notifications, name='all_notifications'),
]

# View images locally.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                                    document_root=settings.MEDIA_ROOT)