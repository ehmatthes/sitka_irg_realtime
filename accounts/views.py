from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import CustomUser
from .forms import CustomUserChangeForm, ProfileForm, InvitationForm


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
    elif request.method == 'POST':
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

@login_required
def invite_user(request):
    """Allow site admins to issue invitations to new users."""

    # Restrict this view to site admins.
    if not request.user.is_site_admin():
        raise Http404

    if request.method == 'GET':
        form = InvitationForm()
    elif request.method == 'POST':
        form = InvitationForm(data=request.POST)
        if form.is_valid():
            form.save()
            # If user exists, reissue invitation email. If they don't exist,
            #   create user and issue invitation email.
            username = form.fields['email'].split('@')[0]
            print(username)

    context = {'form': form}
    return render(request, 'account/invite_user.html', context=context)