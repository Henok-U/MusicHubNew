from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from MusicHub.users.models import User

from .user_factory import UserFactory

fake = Faker()


class TestChangePassword(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.url = reverse("change-password")
        self.user_data = UserFactory()
        self.user_data.set_password("abcABC123*")
        self.user_data.save()
        self.client.force_authenticate(user=self.user_data)

    def test_change_password_success(self):
        data = {
            "old_password": "abcABC123*",
            "password": "password123",
            "confirm_password": "password123",
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email=self.user_data.email)
        self.assertTrue(user.check_password("password123"))

    def test_change_password_wrong_old_password(self):
        data = {
            "old_password": "notavalidpasswor",
            "password": "password123",
            "confirm_password": "password123",
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("password123"))

        data = {
            "old_password": "            ",
            "password": "password123",
            "confirm_password": "password123",
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("password123"))

        data = {
            "old_password": "",
            "password": "password123",
            "confirm_password": "password123",
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("password123"))

        data = {
            "password": "password123",
            "confirm_password": "password123",
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("password123"))

    def test_change_password_invalid_confrim_or_password(self):
        data = {
            "old_password": "abcABC123*",
            "password": "password123",
            "confirm_password": "password1234",
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("password123"))

        data = {
            "old_password": "abcABC123*",
            "password": "password123",
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("password123"))

        data = {
            "old_password": "abcABC123*",
            "password": "",
            "confirm_password": "",
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("password123"))
