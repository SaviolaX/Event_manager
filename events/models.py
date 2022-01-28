from django.db import models

from accounts.models import Profile


class Event(models.Model):
    """Create event"""
    title = models.CharField(max_length=200,
                             blank=False,
                             null=False,
                             verbose_name='event title')
    creator = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='creator',
                                verbose_name='event creator')
    participators = models.ManyToManyField(Profile,
                                           blank=True,
                                           verbose_name='event participators')
    description = models.TextField(blank=True,
                                   verbose_name='event description')
    start = models.CharField(max_length=5,
                             verbose_name='time event starts')
    finish = models.CharField(max_length=5,
                              verbose_name='time event finish')
    event_date = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    privat_event = models.BooleanField(default=False)

    class Meta:
        ordering = ('-timestamp', )

    def __str__(self):
        return f"Event: {self.title} by {self.creator}. \
                Date: {self.event_date}. From:{self.start} to {self.finish}. \
                Privat: {self.privat_event}"


class EventInviteRequest(models.Model):
    """Request event sends to profile"""
    from_event = models.ForeignKey(Event,
                                   on_delete=models.CASCADE,
                                   related_name='from_event',
                                   null=True,
                                   blank=True)
    to_profile = models.ForeignKey(Profile,
                                   on_delete=models.CASCADE,
                                   related_name='to_profile',
                                   null=True,
                                   blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.from_event}"


class JoinEventRequest(models.Model):
    """Request profile sends to event"""
    to_event = models.ForeignKey(Event,
                                 on_delete=models.CASCADE,
                                 related_name='to_event', null=True)
    from_profile = models.ForeignKey(Profile,
                                     on_delete=models.CASCADE,
                                     related_name='from_profile', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.from_profile} to {self.to_event}"
