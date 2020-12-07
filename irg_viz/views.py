from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import Notification


def index(request):
    """Home page for the whole project."""

    notifications = []
    if request.user.is_authenticated:
        notifications = (Notification.objects
                .filter(active=True)
                .order_by('-date_added'))

    context = {
        'notifications': notifications,
    }

    return render(request, 'irg_viz/index.html', context=context)