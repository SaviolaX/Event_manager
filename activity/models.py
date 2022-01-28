from django.db import models

from accounts.models import Profile
from events.models import Event


class EventCreationActivity(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Event creation activities'

    def __str__(self):
        return "{} created event '{}'".format(self.user, self.event)
