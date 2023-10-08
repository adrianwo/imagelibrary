from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.testuser = User.objects.create(username="testuser", password="12345")

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.testuser, User))
        self.assertTrue(hasattr(self.testuser, "profile"))

    def test_profile_basic(self):
        self.testuser.profile.tier = "Basic"
        self.testuser.profile.save()
        profile = self.testuser.profile

        self.assertEqual(profile.height_1, 200)
        self.assertEqual(profile.height_2, 0)
        self.assertFalse(profile.generate_link)
        self.assertFalse(profile.original_link)

    def test_profile_premium(self):
        self.testuser.profile.tier = "Premium"
        self.testuser.profile.save()

        profile = self.testuser.profile
        self.assertEqual(profile.height_1, 200)
        self.assertEqual(profile.height_2, 400)
        self.assertTrue(profile.original_link)
        self.assertFalse(profile.generate_link)

    def test_profile_enterprise(self):
        self.testuser.profile.tier = "Enterprise"
        self.testuser.profile.save()
        profile = self.testuser.profile
        self.assertEqual(profile.height_1, 200)
        self.assertEqual(profile.height_2, 400)
        self.assertTrue(profile.generate_link)
        self.assertTrue(profile.original_link)
