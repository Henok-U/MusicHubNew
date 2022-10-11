from authemail.models import SignupCode
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from MusicHub.users.models import User

from .base_test import CustomApiTestCase


class TestUserRegistrationAPIView(CustomApiTestCase):
    def setUp(self):
        self.set_up("signup")

    def create_signup_code_for_unverified_user(self, user):
        user.is_verified = False
        user.save()
        return SignupCode.objects.create_signup_code(user, "0.0.0.0")

    def verify_user(self, signup_code, status_code):
        response = self.client.get(f"/api/user/signup/verify/?code={signup_code}")
        self.assertEqual(response.status_code, status_code)
        return response

    def is_verified(self, email):
        user = User.objects.get(email=email)
        if user.is_verified:
            return True
        else:
            return False

    def modify_token_date(self, signup_code, hours):
        signup_code.created_at = timezone.now() - timezone.timedelta(hours=hours)
        signup_code.save()
        return signup_code

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
        self.post_and_assert_equal_status_code(data, 201)

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

        self.post_and_assert_equal_status_code(data, 400)

    def test_unique_email_validation(self):
        """
        Test registration with already existing email
        """
        data = {
            "email": "testuser@email.com",
            "password": "abcABC123*",
            "confirm_password": "abcABC123*",
            "first_name": "Vin",
            "last_name": "Diesel",
        }
        self.post_and_assert_equal_status_code(data, 201)

        self.post_and_assert_equal_status_code(data, 400)

    def test_verify_account_with_email_code_success(self):
        signup_code = self.create_signup_code_for_unverified_user(self.user_data)
        self.verify_user(signup_code, 200)
        self.assertEqual(self.is_verified(self.user_data.email), True)

    def test_verify_account_with_expired_code_fail(self):

        signup_code = self.create_signup_code_for_unverified_user(self.user_data)
        signup_code = self.modify_token_date(signup_code, 29)
        self.verify_user(signup_code, 400)
        self.assertEqual(self.is_verified(self.user_data.email), False)

        signup_code = self.create_signup_code_for_unverified_user(self.user_data)
        signup_code = self.modify_token_date(signup_code, 25)
        self.verify_user(signup_code, 400)
        self.assertEqual(self.is_verified(self.user_data.email), False)

        signup_code = self.create_signup_code_for_unverified_user(self.user_data)
        signup_code = self.modify_token_date(signup_code, 50)
        self.verify_user(signup_code, 400)
        self.assertEqual(self.is_verified(self.user_data.email), False)

        signup_code = self.create_signup_code_for_unverified_user(self.user_data)
        signup_code = self.modify_token_date(signup_code, 23)
        self.verify_user(signup_code, 200)
        self.assertEqual(self.is_verified(self.user_data.email), True)

    def test_verify_account_with_email_code_fail(self):
        self.verify_user("invalidcode", 400)

    def test_signup_wrong_data_variants_fail(self):

        data = {
            "email": "testuser2@email.com",
            "password": "abcABC123*",
            "confirm_password": "abcABC123*2131321",
            "first_name": "Vin",
            "last_name": "Diesel",
        }
        self.post_and_assert_equal_status_code(data, 400)
        data = {
            "email": "testuser2@email.com",
            "password": "abcABC123*",
            "first_name": "Vin",
            "last_name": "Diesel",
        }
        self.post_and_assert_equal_status_code(data, 400)
        data = {
            "email": "testuser2@email.com",
            "password": "abcABC123*",
            "confirm_password": "abcABC123*",
            "first_name": "Vin123",
            "last_name": "Diesel$%@",
        }
        self.post_and_assert_equal_status_code(data, 400)
