from django.urls import reverse
from rest_framework.test import APITestCase

from MusicHub.users.models import User

from .user_factory import UserFactory


class CustomApiTestCase(APITestCase):
    def set_up(self, url) -> None:
        self.url = reverse(url)
        self.user_data = UserFactory()
        return super().setUp()

    def patch_and_assert_equal_status_code(self, data, status_code):
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status_code)
        return response

    def get_and_assert_equal_status_code(self, data, status_code):
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status_code)
        return response

    def post_and_assert_equal_status_code(self, data, status_code):
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status_code)
        return response

    def put_and_assert_equal_status_code(self, data, status_code):
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status_code)
        return response


class AuthorizedApiTestCase(CustomApiTestCase):
    def set_up(self, url) -> None:
        self.url = reverse(url)
        self.user_data = UserFactory()
        self.client.force_authenticate(user=self.user_data)
        return super().setUp()

    def check_password_match(self, password, assert_true):
        user = User.objects.get(email=self.user_data.email)
        if assert_true:
            self.assertTrue(user.check_password(password))
        else:
            self.assertFalse(user.check_password(password))
