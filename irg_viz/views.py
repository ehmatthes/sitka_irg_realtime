from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from utils import plot_utils

def index(request):
    """Home page for the whole project."""
    return render(request, 'irg_viz/index.html')

@login_required
def irg_critical_forecast_plot_extended(request):
    """Static critical forecast plot, extended back x hours."""
    return render(request, 'irg_viz/irg_critical_forecast_plot_extended.html')