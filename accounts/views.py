from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


from .models import CustomUser
from .forms import (CustomUserChangeForm, ProfileForm, InvitationForm,
        AcceptInvitationForm)


# --- Helper functions ---

def send_invite_email(request, new_user):
    """Send an invitation email."""
    # Send invitation email.
    subject = "Invitation to the Ḵaasda Héen (Indian River) Monitoring Project"
    invite_link = f"{settings.BASE_URL}/accounts/accept_invitation/"
    email_data = {'user': new_user, 'invite_link': invite_link}
    text_body = render_to_string('account/email/invite_user_body.txt',
            email_data).strip()
    html_body = render_to_string('account/email/invite_user_body.html',
            email_data)

    email_msg = EmailMultiAlternatives(subject=subject,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[new_user.email], body=text_body)

    email_msg.attach_alternative(html_body, "text/html")
    email_msg.send()

    message = "An invitation email has been sent."
    messages.add_message(request, messages.INFO, message,
            extra_tags='invite_message')


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
                # Reissue invitation email to existing user.
                message = f"An account with this email already exists."
                messages.add_message(request, messages.INFO, message,
                        extra_tags='invite_message')

                send_invite_email(request, user)

            except CustomUser.DoesNotExist:
                # Create a new user. Assume this username will be unique for now.
                #   Set a random password, that they'll reset on first login.
                new_user = CustomUser()
                new_user.username = username
                new_user.email = invited_user.email
                new_user.set_unusable_password()
                new_user.save()

                message = f"A new account has been created with the username {new_user.username}."
                messages.add_message(request, messages.INFO, message,
                        extra_tags='invite_message')

                send_invite_email(request, new_user)

            processed_form = True

    context = {'form': form, 'processed_form': processed_form}
    return render(request, 'account/invite_user.html', context=context)

def accept_invitation(request):
    """Allow an invited user to set their password.
    Show a form that asks for email and two passwords.
    On POST, get user with this email. If they don't have a password set,
      use what they've provided and give a success message with a link to 
      login.
      If a user doesn't exist with this password, give a failure alert.
    """

    if request.method == 'GET':
        form = AcceptInvitationForm()

    elif request.method == 'POST':
        form = AcceptInvitationForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password1']
            try:
                # If user exists and has no password, set password and add success
                #   message with link to log in. Include username and password that
                #   was just set.
                user = CustomUser.objects.get(email=email)
                if user.has_usable_password():
                    # For now, handle this the same as user not existing.
                    #   Don't want to let people try others' email addresses
                    #   to find out who has an account.
                    raise CustomUser.DoesNotExist
            except CustomUser.DoesNotExist:
                fail_msg = "Sorry, this request can not be processed."
                messages.add_message(request, messages.INFO, fail_msg,
                        extra_tags='accept_invitation_fail')
            else:
                user.set_password(password)
                user.save()
                success_msg = f"Your password has been set."
                messages.add_message(request, messages.INFO, success_msg,
                        extra_tags='accept_invitation_success')
                success_msg = f" You may now <a href='{settings.LOGIN_URL}'>log in</a>"
                success_msg += f" with the username {user.username} and the password you just created."
                messages.add_message(request, messages.INFO, success_msg,
                        extra_tags='accept_invitation_success')

    context = {'form': form}

    return render(request, 'account/accept_invitation.html', context)