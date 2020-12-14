from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse


def logout_view(request):
    """Log user out, and redirect to home page."""
    logout(request)
    return HttpResponseRedirect(reverse('irg_viz:index'))
