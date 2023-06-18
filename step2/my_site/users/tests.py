from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from models import Profile

class HeartRateViewTestCase(TestCase):
    def setUp(self):
        self.username = 'matvey'
        self.password = 'yashenev'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)

    def test_get_heart_rate(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('heart_rate_api'))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['heart_rate'], self.profile.heart_rate)

    def test_post_heart_rate(self):
        self.client.login(username=self.username, password=self.password)
        data = {'heart_rate': 80}
        response = self.client.post(reverse('heart_rate_api'), data=data)
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.heart_rate, 80)

