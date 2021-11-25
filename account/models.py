from django.db import models
from django.conf import settings


class Profile(models.Model):
    """User's profile"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='user related to profile')
    city = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(
        upload_to='users/', blank=True)
    friends = models.ManyToManyField(
        'Profile', blank=True)

    def __str__(self):
        return self.user.username

    def get_sum_friends(self):
        """Count all friends in friend list"""
        return self.friends.count()

    def get_sum_created_events(self):
        """Count all events created by profile"""
        return self.creator.count()


class FriendRequest(models.Model):
    """Requests a profile sends to another profile"""
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                  related_name='from_user')
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='to_user')
    timestamp = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return f"From {self.from_user} to {self.to_user}"
