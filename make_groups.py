"""Make the groups necessary for the project."""

# Set up django environment.
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "irg_realtime.settings")

import django
django.setup()


from django.contrib.auth.models import Group


def build_all_groups():
    """Build all groups needed, only if they don't already exist."""

    # Site Admins
    #   Members of this group can make notifications, and manage users.
    try:
        site_admins = Group.objects.get(name="Site Admins")
        print("Found group Site Admins.")
    except Group.DoesNotExist:
        site_admins = Group(name='Site Admins')
        site_admins.save()
        print("Created group Site Admins.")


if __name__ == '__main__':
    build_all_groups()