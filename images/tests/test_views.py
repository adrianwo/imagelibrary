from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import json
from images.models import Image, Link
import base64

User = get_user_model()


class ImageViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.userBasic = User.objects.create(
            username="basic", password="pass", is_superuser=True
        )

        Image.objects.create(
            user=self.userBasic,
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
        )

        self.userPremium = User.objects.create(username="premium", password="pass")
        self.userPremium.profile.tier = "Premium"
        self.userPremium.profile.save()

        Image.objects.create(
            user=self.userPremium,
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
        )

        self.userEnterprise = User.objects.create(
            username="enterprise", password="pass"
        )
        self.userEnterprise.profile.tier = "Enterprise"
        self.userEnterprise.profile.save()

        Image.objects.create(
            user=self.userEnterprise,
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
        )

        self.userCustom = User.objects.create(username="custom", password="pass")
        self.userCustom.profile.tier = "Custom"
        self.userCustom.profile.height_1 = 500
        self.userCustom.profile.original_link = True
        self.userCustom.profile.save()

        Image.objects.create(
            user=self.userCustom,
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
        )

    def test_image_list_unauthorized(self):
        response = self.client.get("/images/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_image_list(self):
        self.client.force_login(self.userBasic)
        response = self.client.get("/images/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_image_list_basic(self):
        self.client.force_login(self.userBasic)
        response = self.client.get("/images/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertContains(response, "thumbnail_1")
        self.assertNotContains(response, "thumbnail_2")
        self.assertNotContains(response, "original_image")
        self.assertNotContains(response, "links")

    def test_image_list_premium(self):
        self.client.force_login(self.userPremium)
        response = self.client.get("/images/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertContains(response, "thumbnail_1")
        self.assertContains(response, "thumbnail_2")
        self.assertContains(response, "original_image")
        self.assertNotContains(response, "links")

    def test_image_list_enterprise(self):
        self.client.force_login(self.userEnterprise)
        response = self.client.get("/images/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertContains(response, "thumbnail_1")
        self.assertContains(response, "thumbnail_2")
        self.assertContains(response, "original_image")
        self.assertContains(response, "links")

    def test_image_list_custom(self):
        self.client.force_login(self.userCustom)
        response = self.client.get("/images/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertContains(response, "thumbnail_1")
        self.assertNotContains(response, "thumbnail_2")
        self.assertContains(response, "original_image")
        self.assertNotContains(response, "links")

    def test_image_create_valid(self):
        self.client.force_login(self.userBasic)
        image = SimpleUploadedFile(
            "test_image.jpg",
            content=base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAUA"
                + "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
                + "9TXL0Y4OHwAAAABJRU5ErkJggg=="
            ),
            content_type="image/jpg",
        )

        response = self.client.post("/images/", {"image": image}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
