from authemail.models import PasswordResetCode
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework.test import APITestCase

from MusicHub.users.models import User

from .user_factory import UserFactory

fake = Faker()


class TestUserRegistrationAPIView(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.url = reverse("reset-password")
        self.user_data = UserFactory()

    def test_reset_password_success(self):
        response = self.client.post(self.url, {"email": self.user_data})
        self.assertEqual(response.status_code, 200)
        reset_code = PasswordResetCode.objects.get(user=self.user_data)
        data = {"password": "newpassword123", "confirm_password": "newpassword123"}
        response = self.client.put(f"{self.url}?code={reset_code}", data=data)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email=self.user_data.email)
        self.assertTrue(user.check_password("newpassword123"))

    def test_reset_password_code_email_not_found_or_not_valid_email(self):
        response = self.client.post(self.url, {"test": "test"})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(self.url, {"email": "notavalidemail"})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(self.url, {"email": "notavalidemail@gmail.com"})
        self.assertEqual(response.status_code, 400)

    def test_reset_password_code_expired(self):
        response = self.client.post(self.url, {"email": self.user_data})
        self.assertEqual(response.status_code, 200)
        reset_code = PasswordResetCode.objects.get(user=self.user_data)
        reset_code.created_at = timezone.now() - timezone.timedelta(days=2)
        reset_code.save()
        data = {"password": "newpassword123", "confirm_password": "newpassword123"}
        response = self.client.put(f"{self.url}?code={reset_code}", data=data)
        self.assertEqual(response.status_code, 400)

    def test_reset_password_passwords_validation_fails(self):
        response = self.client.post(self.url, {"email": self.user_data})
        self.assertEqual(response.status_code, 200)
        reset_code = PasswordResetCode.objects.get(user=self.user_data)

        data = {"password": "newpassword123", "confirm_password": "notthesamepassword"}
        response = self.client.put(f"{self.url}?code={reset_code}", data=data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("newpassword123"))

        data = {"password": "", "confirm_password": ""}
        response = self.client.put(f"{self.url}?code={reset_code}", data=data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("newpassword123"))

        data = {"password": "password123", "confirm_password": ""}
        response = self.client.put(f"{self.url}?code={reset_code}", data=data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("newpassword123"))

        response = self.client.put(f"{self.url}?code={reset_code}")
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(email=self.user_data.email)
        self.assertFalse(user.check_password("newpassword123"))

        response = self.client.put(f"{self.url}")
        self.assertEqual(response.status_code, 400)

        response = self.client.put(f"{self.url}?code=invalidcode")
        self.assertEqual(response.status_code, 400)
