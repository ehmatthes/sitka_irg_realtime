"""Make sample users for the project."""

# Set up django environment.
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "irg_realtime.settings")

import django
django.setup()

from django.contrib.auth.models import Group
from django.db.utils import IntegrityError

from accounts.models import CustomUser


# Create a regular user, superuser, and site admin user.
try:
    user = CustomUser.objects.create_user('sample_user', 'sample_user@example.com',
            'sample_user')
    print('Created regular user:', user)
except IntegrityError:
    print('Regular user already exists.')

try:
    user = CustomUser.objects.create_superuser('sample_su', 'sample_su@example.com',
            'sample_su')
    print('Created superuser:', user)
except IntegrityError:
    print('Superuser already exists.')

try:
    user = CustomUser.objects.create_user('sample_admin', 'sample_admin@example.com',
            'sample_admin')
except IntegrityError:
    print('Site admin user already exists.')
else:
    site_admins = Group.objects.get(name='Site Admins')
    site_admins.user_set.add(user)
    print('Created site admin user:', user)
