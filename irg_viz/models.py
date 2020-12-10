from django.db import models
from users.models import CustomUser


class Notification(models.Model):
    """Notifications that will be placed under the main visualization.
    See documentation: https://github.com/ehmatthes/sitka_irg_realtime/blob/main/my_docs/notifications.md

    Be really careful with these, as they will be written and read during
      heavy rain events that could lead to landslides.
    
    DEV: Should probably record a timestamp whenever value of active changes.
    """

    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    date_added = models.DateTimeField(auto_now_add=True)

    # Most notifications should start out active, and then become permanently
    #   inactive. Notifications should not be reused, unless we recognize the
    #   need for a default set of generic notifications. Most of those, 
    #   however, should probably be incorporated into standard text on the
    #   site.
    # A notification may be set inactive while drafting it, and consulting with
    #   others.
    active = models.BooleanField(default=True)


    def __str__(self):
        """Default representation of notification."""
        if len(self.text) <= 50:
            return self.text
        else:
            return self.text[:50] + "..."