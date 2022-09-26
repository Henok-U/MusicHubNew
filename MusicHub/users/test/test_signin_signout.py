from queue import Empty

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from MusicHub.users.models import User


class TestSigninSignoutAPIView(APITestCase):
    def setUp(self):
        # Verified User
        self.verified_user = User.objects.create_user(
            first_name="verified",
            last_name="user",
            email="verified@email.com",
            password="abcABC123*",
            is_verified=True,
        )
        self.verified_user.save()

        # Unverified User
        self.unverified_user = User.objects.create_user(
            first_name="unverified",
            last_name="user",
            email="unverified@email.com",
            password="unverifiedpass123*",
        )
        self.unverified_user.save()

        # Inactive User
        self.inactive_user = User.objects.create_user(
            first_name="invalid",
            last_name="user",
            email="inactive@email.com",
            password="inactivepass123*",
            is_active=False,
        )
        self.inactive_user.save()

        self.signin_url = reverse("signin")
        self.signout_url = reverse("signout")

    def test_signin_invalid_credentials(self):
        # invalid password
        data = {
            "email": self.verified_user.email,
            "password": "wrong_pass",
        }
        response = self.client.post(self.signin_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Invalid credentials, unable to signin."
        )

        # invalid email
        data = {
            "email": "invalid@email.com",
            "password": "abcABC123*",
        }
        response = self.client.post(self.signin_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Invalid credentials, unable to signin."
        )

    def test_signin_signout(self):
        # user sign in
        data = {
            "email": self.verified_user.email,
            "password": "abcABC123*",
        }
        response = self.client.post(self.signin_url, data)

        self.assertTrue(self.verified_user is not Empty)
        self.assertTrue(self.verified_user.is_authenticated)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

        token = response.data["token"]

        # user sign out
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.get(self.signout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Success"], "User signed out.")

    def signin_unverified_inactive(self):
        # unverified user
        data = {
            "email": self.unverified_user.email,
            "password": "unverifiedpass123*",
        }
        response = self.client.post(self.signin_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Unverified user account.")

        # Inactive User
        data = {
            "email": self.inactive_user.email,
            "password": "unverifiedpass123*",
        }
        response = self.client.post(self.signin_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Inactive user account.")

    def test_signout_no_token(self):
        response = self.client.get(self.signout_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"],
            "Authentication credentials were not provided.",
        )
