from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .forms import CustomUserCreationForm
from .models import CustomUser


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.   
        form = CustomUserCreationForm()
    else:
        # Process completed form.
        form = CustomUserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('learning_logs:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@login_required
def request_password_reset(request):
    """Request a password reset."""

    # Anyone logged in can request this page, and there's not data to send.
    return render(request, 'registration/request_password_reset.html')

def send_password_reset(request, user_id):
    """Send a password reset email."""

    user = CustomUser.objects.get(id=user_id)

    # Make sure requested user matches current user.
    if user != request.user:
        return Http404

    print('\n\nsending password reset email')

    from django.contrib.auth.forms import PasswordResetForm

    print('user email:', user.email)
    form = PasswordResetForm(data={'email': user.email})
    if form.is_valid():
        # Build required arts.
        # From: https://github.com/django/django/blob/master/django/contrib/auth/views.py
        from django.contrib.auth.tokens import default_token_generator
        opts = {
            'use_https': request.is_secure(),
            'token_generator': default_token_generator,
            'from_email': None,
            'email_template_name': 'registration/password_reset_email.html',
            'subject_template_name': 'registration/password_reset_subject.txt',
            'request': request,
            'html_email_template_name': None,
            'extra_email_context': None,
        }
        form.save(**opts)

        print('valid form')
        from django.views.generic.edit import FormView
        form_view = FormView()
        return form_view.form_valid(form)
        print('wtf')
    else:
        print('invalid form')
        print(form)

    return HttpResponseRedirect(reverse('users:password_reset_sent'))

@login_required
def password_reset_sent(request):
    """Confirmt that a password reset email was sent."""

    return render(request, 'registration/password_reset_sent.html')


