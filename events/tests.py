from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


from .models import Event
from accounts.models import Profile


class CreateEventTest(TestCase):

    def test_create_user(self):
        testuser1 = User.objects.create_user(
        username='testuser1', password='abc123')
        testuser1.save()

        test_profile = Profile.objects.create(user=testuser1, 
                                              city='Poltava')


        event = Event.objects.create(
            title='Test_title',
            creator=test_profile,
            description='Test_text',
            start='20:00',
            finish='22:00',
            event_date='21.02.2020',
            privat_event=False
        )

    def test_current_event(self):

        test_evet = Event.objects.get(id=1)
        title = f"{test_evet.title}"
        creator = f"{test_evet.creator}"
        description = f"{test_evet.description}"
        start = f"{test_evet.start}"
        finish = f"{test_evet.finish}"
        privat_event = f"{test_evet.privat_event}"

        self.assertEqual(test_evet.title, 'Test_title')
        self.assertEqual(test_evet.creator, test_profile)
        self.assertEqual(test_evet.description, 'Test_text')
        self.assertEqual(test_evet.start, '20:00')
        self.assertEqual(test_evet.finish, '22:00')
        self.assertEqual(test_evet.event_date, '21.02.2020')
        self.assertEqual(test_evet.privat_event, False)
