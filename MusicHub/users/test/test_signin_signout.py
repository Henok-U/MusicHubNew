from django.urls import reverse
from rest_framework import status

from MusicHub.users.test.base_test import CustomApiTestCase

from .user_factory import UserFactory


class TestSigninSignoutAPIView(CustomApiTestCase):
    def setUp(self):
        self.set_up("signin")
        self.verified_user = self.user_data
        self.unverified_user = UserFactory(is_verified=False)
        self.inactive_user = UserFactory(is_active=False)

    def test_signin_invalid_credentials(self):
        # invalid password
        self.post_and_assert_equal_status_code(
            data={
                "email": self.verified_user.email,
                "password": "wrong_pass",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

        # invalid email
        self.post_and_assert_equal_status_code(
            data={
                "email": "invalid@email.com",
                "password": "abcABC123*",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    def test_signin_signout(self):
        # user sign in
        response = self.post_and_assert_equal_status_code(
            data={
                "email": self.verified_user.email,
                "password": "abcABC123*",
            },
            status_code=status.HTTP_200_OK,
        )
        self.assertTrue(self.verified_user.is_authenticated)
        self.assertIn("token", response.data)

        token = response.data["token"]

        # user sign out
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.url = reverse("signout")
        self.get_and_assert_equal_status_code(status_code=status.HTTP_200_OK)

    def signin_unverified_inactive(self):
        self.url = reverse("signin")

        # unverified user
        self.post_and_assert_equal_status_code(
            data={
                "email": self.unverified_user.email,
                "password": "unverifiedpass123*",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

        # Inactive User
        self.post_and_assert_equal_status_code(
            data={
                "email": self.inactive_user.email,
                "password": "unverifiedpass123*",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    def test_signout_no_token(self):
        self.url = reverse("signout")
        self.get_and_assert_equal_status_code(status_code=status.HTTP_401_UNAUTHORIZED)
