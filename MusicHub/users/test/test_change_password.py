from rest_framework import status

from .base_test import AuthorizedApiTestCase


class TestChangePassword(AuthorizedApiTestCase):
    def setUp(self):
        self.set_up("change-password")

    def test_change_password_success(self):
        data = {
            "old_password": "abcABC123*",
            "password": "password123",
            "confirm_password": "password123",
        }
        self.patch_and_assert_equal_status_code(data, status.HTTP_200_OK)
        self.check_password_match("password123", True)

    def test_change_password_wrong_old_password(self):
        data = {
            "old_password": "notavalidpasswor",
            "password": "password123",
            "confirm_password": "password123",
        }
        self.patch_and_assert_equal_status_code(data, status.HTTP_400_BAD_REQUEST)
        self.check_password_match("password123", False)

        data = {
            "old_password": "            ",
            "password": "password123",
            "confirm_password": "password123",
        }
        self.patch_and_assert_equal_status_code(data, status.HTTP_400_BAD_REQUEST)
        self.check_password_match("password123", False)

        data = {
            "old_password": "",
            "password": "password123",
            "confirm_password": "password123",
        }
        self.patch_and_assert_equal_status_code(data, status.HTTP_400_BAD_REQUEST)
        self.check_password_match("password123", False)

        data = {
            "password": "password123",
            "confirm_password": "password123",
        }
        self.patch_and_assert_equal_status_code(data, status.HTTP_400_BAD_REQUEST)
        self.check_password_match("password123", False)

    def test_change_password_invalid_confrim_or_password(self):
        data = {
            "old_password": "abcABC123*",
            "password": "password123",
            "confirm_password": "password1234",
        }
        self.patch_and_assert_equal_status_code(data, status.HTTP_400_BAD_REQUEST)
        self.check_password_match("password123", False)

        data = {
            "old_password": "abcABC123*",
            "password": "password123",
        }
        self.patch_and_assert_equal_status_code(data, status.HTTP_400_BAD_REQUEST)
        self.check_password_match("password123", False)

        data = {
            "old_password": "abcABC123*",
            "password": "",
            "confirm_password": "",
        }
        self.patch_and_assert_equal_status_code(data, status.HTTP_400_BAD_REQUEST)
        self.check_password_match("password123", False)
