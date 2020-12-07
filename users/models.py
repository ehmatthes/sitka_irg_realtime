from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Customize user model.
    """

    pass

    def __str__(self):
        """Admin representation of user."""
        return self.username

    def is_site_admin(self):
        """Check if user is a site administrator."""
        pass

