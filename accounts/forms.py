from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from allauth.account.forms import SetPasswordForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', )


class ProfileForm(forms.ModelForm):
    """Form for editing a user's profile."""

    class Meta:
        model = CustomUser
        fields = ('email', )


class InvitationForm(forms.ModelForm):
    """Form for issuing an invitation to a new user.
    Should also work for reissuing an invitation.
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', )


class AcceptInvitationForm(SetPasswordForm):
    email = forms.EmailField(required=True)

    field_order = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
