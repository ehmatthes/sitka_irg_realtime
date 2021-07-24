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

    # Historical example pages.
    path('hist_examples/', views.hist_examples, name='hist_examples'),
    path('hist_examples_092019/', views.hist_examples_092019,
            name='hist_examples_092019'),
    path('hist_examples_091316/', views.hist_examples_091316,
            name='hist_examples_091316'),
    path('hist_examples_072620/', views.hist_examples_072620,
            name='hist_examples_072620'),
    path('hist_examples_072020/', views.hist_examples_072020,
            name='hist_examples_072020'),
    path('hist_examples_091616/', views.hist_examples_091616,
            name='hist_examples_091616'),

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