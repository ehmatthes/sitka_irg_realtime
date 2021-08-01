from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse


from .models import Notification
from .forms import NotificationForm

def index(request):
    """Home page for the whole project."""
    notifications = (Notification.objects
            .filter(active=True)
            .order_by('-date_added'))

    context = {
        'notifications': notifications,
    }

    return render(request, 'irg_viz/index.html', context=context)

def about(request):
    """About the project."""
    context = {}
    return render(request, 'irg_viz/about.html', context=context)

def hist_examples(request):
    """List of historical examples."""
    context = {}
    return render(request, 'irg_viz/hist_examples.html', context=context)

def hist_examples_092019(request):
    """Historical example page focusing on Medvejie slide, 9/20/19."""
    context = {}
    return render(request, 'irg_viz/hist_examples_092019.html',
            context=context)

def hist_examples_091316(request):
    """Historical example page focusing on critical unassociated event,
    9/13/2016.
    """
    context = {}
    return render(request, 'irg_viz/hist_examples_091316.html',
            context=context)

def hist_examples_072620(request):
    """Historical example page focusing on almost-critical event,
    7/26/2020.
    """
    context = {}
    return render(request, 'irg_viz/hist_examples_072620.html',
            context=context)

def hist_examples_072020(request):
    """Historical example page focusing on completely noncritical event,
    7/20/2020.
    """
    context = {}
    return render(request, 'irg_viz/hist_examples_072020.html',
            context=context)

def hist_examples_091616(request):
    """Historical example page focusing on unassociated slide
    9/16/2016.
    """
    context = {}
    return render(request, 'irg_viz/hist_examples_091616.html',
            context=context)

def critical_factors(request):
    """Discussion of how critical factors are used in the current analysis.
    """
    context = {}
    return render(request, 'irg_viz/critical_factors.html', context=context)

def interpreting_graph(request):
    """Further explanation about how to interpret the graph."""
    context = {}
    return render(request, 'irg_viz/interpreting_graph.html', context=context)

def project_timeline(request):
    """Timeline of the project."""
    context = {}
    return render(request, 'irg_viz/project_timeline.html', context=context)

def next_steps(request):
    """Road map for the project."""
    context = {}
    return render(request, 'irg_viz/next_steps.html', context=context)

def disclaimer(request):
    """State known limitations of the project."""
    context = {}
    return render(request, 'irg_viz/disclaimer.html', context=context)

def contact(request):
    """Simple contact page."""
    context = {}
    return render(request, 'irg_viz/contact.html', context=context)

@login_required
def new_notification(request):
    """Create a new notification.
    """

    # Only members of site_admin group can create notifications.
    if not request.user.is_site_admin():
        raise Http404

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = NotificationForm()
    else:
        # POST data submitted; process data.
        form = NotificationForm(request.POST)
        if form.is_valid():
            new_notification = form.save(commit=False)
            new_notification.author = request.user
            new_notification.save()

            return HttpResponseRedirect(reverse('irg_viz:index'))

    context = {'form': form}
    return render(request, 'irg_viz/new_notification.html', context)

@login_required
def edit_notification(request, notification_id):
    """Edit an existing notification."""

    # Only members of site_admin group can create notifications.
    if not request.user.is_site_admin():
        raise Http404

    # Any site admin can modify any notification.
    notification = Notification.objects.get(id=notification_id)

    if request.method != 'POST':
        # No data submitted; create a filled in form.
        form = NotificationForm(instance=notification)
    else:
        # POST data submitted; process data.
        form = NotificationForm(instance=notification, data=request.POST)
        if form.is_valid():
            modified_notification = form.save()

            return HttpResponseRedirect(reverse('irg_viz:index'))

    context = {'form': form, 'notification': notification}
    return render(request, 'irg_viz/edit_notification.html', context)

@login_required
def all_notifications(request):
    """See all notifications that have been issued.
    No pagination for now.
    """

    # Only members of site_admin group can view inactive notifications.
    if not request.user.is_site_admin():
        raise Http404

    notifications = Notification.objects.all().order_by('-date_added')

    context = {'notifications': notifications}

    return render(request, 'irg_viz/all_notifications.html', context)