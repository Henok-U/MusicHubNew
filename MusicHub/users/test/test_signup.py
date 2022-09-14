from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUserRegistrationAPIView(APITestCase):
    url = reverse("create")

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
        response = self.client.post(reverse("create"), data_two)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
