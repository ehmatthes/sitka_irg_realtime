from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import logout
from django.urls import reverse

from .models import CustomUser
from .forms import CustomUserChangeForm, ProfileForm


def logout_view(request):
    """Log user out, and redirect to home page."""
    logout(request)
    return HttpResponseRedirect(reverse('irg_viz:index'))

def profile(request):
    """Simple user profile page."""
    return render(request, 'account/profile.html')

def edit_profile(request):
    """Simple edit user profile page.
    Can only change email at the moment.
    """

    if request.method == 'GET':
        form = ProfileForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:profile'))

    print(form.is_valid())

    context = {'form': form}
    return render(request, 'account/edit_profile.html', context=context)

def signup(request):
    """Simple view to override signup from allauth, since this project
    is invite-only.
    """
    raise Http404