"""Make the sites necessary for the project.
This is really for django-allauth.
"""

# Set up django environment.
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "irg_realtime.settings")

import django
django.setup()


from django.contrib.sites.models import Site

def modify_site():
    """Modify existing site with id 1 to represent local site.
    """
    site = Site.objects.get(id=1)
    site.domain = 'http://localhost:8000'
    site.name = 'Localhost'
    site.save()

    print(f"Modifed site with id 1 to {site.domain}, {site.name}.")


if __name__ == '__main__':
    modify_site()