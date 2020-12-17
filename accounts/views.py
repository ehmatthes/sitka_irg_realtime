from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings


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

    # Clear messages.
    for message in messages.get_messages(request):
        message.used = True

    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'GET':
        form = InvitationForm()
        processed_form = False
    elif request.method == 'POST':
        form = InvitationForm(data=request.POST)
        if form.is_valid():

            # Get form data without saving user. Could just pull POST data,
            #   but this is a familiar workflow.
            invited_user = form.save(commit=False)
            # If user exists, reissue invitation email. If they don't exist,
            #   create user and issue invitation email.
            username = invited_user.email.split('@')[0]
            try:
                user = CustomUser.objects.get(email=invited_user.email)
                print("Found existing user:", user)
                # Reissue invitation email to existing user.
                message = f"An account with this email already exists. A new invitation email has been sent."
                messages.add_message(request, messages.INFO, message,
                        extra_tags='invite_message')
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

                message = f"A new account has been created with the username {new_user.username}."
                messages.add_message(request, messages.INFO, message,
                        extra_tags='invite_message')

                # Send invitation email.
                #   DEV: here.
                import os
                print(os.getcwd())
                with open('accounts/templates/account/email/initial_invite_message.html') as f:
                    body = f.read()
                subject = "Invitation to the Ḵaasda Héen (Indian River) Monitoring Project"

                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                        (new_user.email, ), html_message=body)


                message = "An invitation email has been sent."
                messages.add_message(request, messages.INFO, message,
                        extra_tags='invite_message')

            processed_form = True





    context = {'form': form, 'processed_form': processed_form}
    return render(request, 'account/invite_user.html', context=context)