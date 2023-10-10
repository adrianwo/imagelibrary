from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from django.utils import timezone
from datetime import datetime


from images.models import Image, Link


class ImageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password")

    def test_image_creation(self):
        image = Image.objects.create(
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
            user=self.user,
        )
        self.assertTrue(isinstance(image, Image))
        # self.assertTrue(hasattr(self.testuser, "profile"))

    def test_image_ext_validator_ok(self):
        image = Image.objects.create(
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
            user=self.user,
        )
        self.assertTrue(isinstance(image, Image))

        image = Image.objects.create(
            image=SimpleUploadedFile("test_image.jpeg", b"file_content"),
            user=self.user,
        )
        self.assertTrue(isinstance(image, Image))

        image = Image.objects.create(
            image=SimpleUploadedFile("test_image.png", b"file_content"),
            user=self.user,
        )
        self.assertTrue(isinstance(image, Image))

    def test_image_ext_validator_fail(self):
        with self.assertRaises(ValidationError):
            image = Image.objects.create(
                image=SimpleUploadedFile("test_image.gif", b"file_content"),
                user=self.user,
            )
            image.full_clean()

    def test_image_user_not_allowed(self):
        user2 = User.objects.create(username="user_2", password="pass")
        image = Image.objects.create(
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
            user=self.user,
        )
        is_allowed = image.is_user_allowed(user2)
        self.assertFalse(is_allowed)


class LinkTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password")
        self.image = Image.objects.create(
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
            user=self.user,
        )

    def test_link_creation(self):
        link = Link.objects.create(image=self.image, valid=300)
        self.assertTrue(isinstance(link, Link))

    def test_valid_(self):
        with self.assertRaises(ValidationError):
            link = Link.objects.create(image=self.image, valid=100)
            link.full_clean()
        with self.assertRaises(ValidationError):
            link = Link.objects.create(image=self.image, valid=40_000)
            link.full_clean()

    @patch("images.models.timezone.now")
    def test_link_expiration(self, now_mock):
        now_mock.return_value = timezone.make_aware(datetime(2023, 10, 10, 18, 0))
        link = Link.objects.create(image=self.image, valid=400)

        now_mock.return_value = timezone.make_aware(datetime(2023, 10, 10, 18, 1))

        link_1 = Link.objects.get(id=link.id)
        self.assertIsInstance(link_1, Link)

        now_mock.return_value = timezone.make_aware(datetime(2023, 10, 10, 18, 10))
        with self.assertRaises(Link.DoesNotExist):
            Link.objects.get(id=link.id)
