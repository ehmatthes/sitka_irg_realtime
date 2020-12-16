from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
            invited_user = form.save(commit=False)
            # If user exists, reissue invitation email. If they don't exist,
            #   create user and issue invitation email.
            username = invited_user.email.split('@')[0]
            try:
                user = CustomUser.objects.get(email=invited_user.email)
                print("Found existing user:", user)
                # Reissue invitation email to existing user.
                message = f"{user.username} already has an account, and has been reissued an invitation."
                messages.add_message(request, messages.INFO, message)
            except CustomUser.DoesNotExist:
                print("Can not find existing user.")
                # Create a new user. Assume this username will be unique for now.
                #   Set a random password, that they'll reset on first login.
                new_user = CustomUser()
                new_user.username = username
                new_user.email = invited_user.email
                new_user.set_unusable_password()
                new_user.save()
                print("  Saved new user:", new_user.username, new_user.email)
                message = f"Created new user with username {new_user.username}."
                messages.add_message(request, messages.INFO, message)



    context = {'form': form}
    return render(request, 'account/invite_user.html', context=context)