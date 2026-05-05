from django.test import TestCase
from django.contrib.auth.models import User

from .models import Profile


class ProfileModelTests(TestCase):
    def test_profile_str(self):
        user = User.objects.create_user(username="david", password="pass12345")
        profile = Profile.objects.create(user=user, bio="hi")
        self.assertEqual(str(profile), "david Profile")