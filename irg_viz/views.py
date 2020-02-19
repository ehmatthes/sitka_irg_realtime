from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from utils import plot_utils

def index(request):
    """Home page for the whole project."""
    return render(request, 'irg_viz/index.html')

@login_required
def simple_irg_plot(request):
    """Simple plot of the river gauge."""
    return render(request, 'irg_viz/simple_irg_plot.html')
