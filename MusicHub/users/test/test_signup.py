from time import time

from authemail.models import SignupCode
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from MusicHub.users.models import User


class TestUserRegistrationAPIView(APITestCase):
    url = reverse("signup")

    def test_valid_user_registration(self):
        """
        Test to verify valid user registration
        """

        data = {
            "email": "testuser@email.com",
            "password": "abcABC123*",
            "confirm_password": "abcABC123*",
            "first_name": "Vin",
            "last_name": "Diesel",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "id")
        self.assertContains(response, "email")
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")

    def test_invalid_user_registration(self):
        """
        Test to verify user registration with invalid password
        """

        data = {
            "email": "testuser@email.com",
            "password": "ab",
            "confirm_password": "ab",
            "first_name": "Vin",
            "last_name": "Diesel",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_email_validation(self):
        """
        Test registration with already existing email
        """

        # user one ---------------------------------------------------
        data_one = {
            "email": "testuser@email.com",
            "password": "abcABC123*",
            "confirm_password": "abcABC123*",
            "first_name": "Vin",
            "last_name": "Diesel",
        }
        response = self.client.post(self.url, data_one)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "email")

        # user two ---------------------------------------------------
        data_two = {
            "email": "testuser@email.com",
            "password": "abcABC123*",
            "confirm_password": "abcABC123*",
            "first_name": "Vin",
            "last_name": "Diesel",
        }
        response = self.client.post(reverse("signup"), data_two)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_account_with_email_code_success(self):

        data = {
            "email": "testuser2@email.com",
            "password": "abcABC123*",
            "confirm_password": "abcABC123*",
            "first_name": "Vin",
            "last_name": "Diesel",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(email="testuser2@email.com")
        self.assertEqual(user.is_verified, False)
        verify_token = SignupCode.objects.get(user=user)
        response = self.client.get(f"/api/user/signup/verify/?code={verify_token}")
        user = User.objects.get(email="testuser2@email.com")
        self.assertEqual(user.is_verified, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_account_with_expired_code_fail(self):
        data = {
            "email": "testuser2@email.com",
            "password": "abcABC123*",
            "confirm_password": "abcABC123*",
            "first_name": "Vin",
            "last_name": "Diesel",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(email="testuser2@email.com")
        self.assertEqual(user.is_verified, False)
        verify_token = SignupCode.objects.get(user=user)
        verify_token.created_at = timezone.now() - timezone.timedelta(days=2)
        verify_token.save()
        response = self.client.get(f"/api/user/signup/verify/?code={verify_token}")
        user = User.objects.get(email="testuser2@email.com")
        self.assertEqual(user.is_verified, False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_account_with_email_code_fail(self):
        data = {
            "email": "testuser2@email.com",
            "password": "abcABC123*",
            "confirm_password": "abcABC123*",
            "first_name": "Vin",
            "last_name": "Diesel",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(email="testuser2@email.com")
        self.assertEqual(user.is_verified, False)
        response = self.client.get(f"/api/user/signup/verify/?code=somenotvalidcode")
        user = User.objects.get(email="testuser2@email.com")
        self.assertEqual(user.is_verified, False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
