from django.test import TestCase
from django.contrib.auth.models import User

# from ..models import Profile


class ProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        print(self.user)
