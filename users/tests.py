from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class ProfileSignalTests(TestCase):
    def test_profile_is_created_for_new_user(self):
        user = User.objects.create_user(username="david", password="pass12345")

        # signal should have created it automatically
        self.assertTrue(Profile.objects.filter(user=user).exists())
        profile = Profile.objects.get(user=user)
        self.assertEqual(str(profile), "david Profile")

    def test_only_one_profile_per_user(self):
        user = User.objects.create_user(username="eva", password="pass12345")
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)