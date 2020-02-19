from django.shortcuts import render

def index(request):
    """Home page for the whole project."""
    return render(request, 'irg_viz/index.html')
