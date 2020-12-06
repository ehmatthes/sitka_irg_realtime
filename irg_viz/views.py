from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    """Home page for the whole project."""
    return render(request, 'irg_viz/index.html')