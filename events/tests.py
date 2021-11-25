from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Event
from account.models import Profile


class CreateEventTest(TestCase):
    def test_create_event(self):
        User = get_user_model()
        profile = Profile.objects.create(

            )
        event = Event.objects.create(
            title='Test_title',
            creator=profile,
            description='Test_text',
            start='20:00',
            finish='22:00',
            event_date='21.02.2020',
            privat_event=False
        )
        self.assertEqual(event.title, 'Test_title')
        self.assertEqual(event.title, 'Test_user')
        self.assertEqual(event.creator, 'Test_text')
        self.assertEqual(event.start, '20:00')
        self.assertEqual(event.finish, '22:00')
        self.assertEqual(event.event_date, '21.02.2020')
        self.assertEqual(event.privat_event, False)
