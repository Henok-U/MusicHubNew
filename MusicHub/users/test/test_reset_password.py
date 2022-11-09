from authemail.models import PasswordResetCode
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework.test import APITestCase

from MusicHub.users.models import User

from .user_factory import UserFactory

fake = Faker()

from rest_framework import status

from .base_test import CustomApiTestCase


class TestUserRegistrationAPIView(CustomApiTestCase):
    def setUp(self):
        self.set_up("reset-password")

    def reset_password_and_get_user(self, token, data, status_code):
        response = self.client.patch(f"{self.url}?code={token}", data=data)
        self.assertEqual(response.status_code, status_code)
        return User.objects.get(email=self.user_data.email)

    def modify_reset_code_date(self, days):
        reset_code = PasswordResetCode.objects.get(user=self.user_data)
        reset_code.created_at = timezone.now() - timezone.timedelta(days=days)
        reset_code.save()
        return reset_code

    def test_reset_password_success(self):
        self.post_and_assert_equal_status_code({"email": self.user_data}, 200)

        reset_code = PasswordResetCode.objects.get(user=self.user_data)
        data = {"password": "newpassword123", "confirm_password": "newpassword123"}

        user = self.reset_password_and_get_user(reset_code, data, 200)

        self.assertTrue(user.check_password("newpassword123"))

    def test_reset_password_code_email_not_found_or_not_valid_email(self):

        self.post_and_assert_equal_status_code({"test": "test"}, 400)

        self.post_and_assert_equal_status_code({"email": "notavalidemail"}, 400)

        self.post_and_assert_equal_status_code(
            {"email": "notavalidemail@gmail.com"}, 400
        )

    def test_reset_password_code_expired(self):
        self.post_and_assert_equal_status_code({"email": self.user_data}, 200)

        data = {"password": "newpassword123", "confirm_password": "newpassword123"}
        reset_code = self.modify_reset_code_date(2)

        user = self.reset_password_and_get_user(reset_code, data, 400)
        self.assertFalse(user.check_password("newpassword123"))

    def test_reset_password_passwords_validation_fails(self):
        self.post_and_assert_equal_status_code({"email": self.user_data}, 200)
        reset_code = PasswordResetCode.objects.get(user=self.user_data)

        data = {"password": "newpassword123", "confirm_password": "notthesamepassword"}
        user = self.reset_password_and_get_user(reset_code, data, 400)

        self.assertFalse(user.check_password("newpassword123"))

        data = {"password": "", "confirm_password": ""}
        user = self.reset_password_and_get_user(reset_code, data, 400)
        self.assertFalse(user.check_password("newpassword123"))

        data = {"password": "password123", "confirm_password": ""}
        user = self.reset_password_and_get_user(reset_code, data, 400)
        self.assertFalse(user.check_password("newpassword123"))

        user = self.reset_password_and_get_user(reset_code, None, 400)
        self.assertFalse(user.check_password("newpassword123"))

        response = self.client.patch(f"{self.url}")
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(f"{self.url}?code=invalidcode")
        self.assertEqual(response.status_code, 400)
