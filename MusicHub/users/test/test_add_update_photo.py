from faker import Faker
from rest_framework.test import APITestCase
from .user_factory import UserFactory
from django.urls import reverse
from pathlib import Path
from os.path import join
import os
import io
from ..models import User

fake = Faker()


class TestUserRegistrationAPIView(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.url = reverse("upload-photo")
        self.user_data = UserFactory()

    def test_add_and_update_photo_success(self):
        self.client.force_authenticate(user=self.user_data)
        picture = Path(__file__).resolve().parent.parent.parent
        picture = join(os.path.dirname(picture), "media/users/avatar/")

        with open(f"{picture}test.jpg", "rb") as fp:
            response = self.client.patch(path=self.url, data={"picture": fp})

            self.assertEqual(response.status_code, 200)
            user = User.objects.get(email=self.user_data.email)
            old_picture = user.profile_avatar

        with open(f"{picture}test2.jpg", "rb") as fpp:
            response = self.client.patch(path=self.url, data={"picture": fpp})
            self.assertEqual(response.status_code, 200)
        user = User.objects.get(email=self.user_data.email)
        new_picture = user.profile_avatar
        user.profile_avatar.delete()
        self.assertNotEqual(old_picture.name, new_picture.name)

    def test_add_invalid_photo_format_fail(self):
        self.client.force_authenticate(user=self.user_data)
        picture = Path(__file__).resolve().parent.parent.parent
        picture = join(os.path.dirname(picture), "media/users/avatar/")

        with open(f"{picture}image.jfif", "rb") as fpp:

            response = self.client.patch(path=self.url, data={"picture": fpp})

            self.assertEqual(response.status_code, 400)

    def test_add_picture_too_big_fail(self):

        self.client.force_authenticate(user=self.user_data)
        picture = Path(__file__).resolve().parent.parent.parent
        picture = join(os.path.dirname(picture), "media/users/avatar/")
        with open(f"{picture}testtt.jpg", "rb") as fppp:
            response = self.client.patch(path=self.url, data={"picture": fppp})

            self.assertEqual(response.status_code, 400)
