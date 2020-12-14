"""irg_realtime URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # My accounts app comes before django-allauth, to override some urls
    #   such as logout/.
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    
    path('', include('irg_viz.urls')),
]
