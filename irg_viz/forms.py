"""Forms for irg_viz app."""

from django import forms

from .models import Notification


class NotificationForm(forms.ModelForm):
    """Form for creating a new notification.
    """

    class Meta:
        model = Notification
        fields = ['text', 'active']
