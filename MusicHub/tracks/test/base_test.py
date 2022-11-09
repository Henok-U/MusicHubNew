from django.urls import reverse
from rest_framework.test import APITestCase

from ...users.test.user_factory import UserFactory


class AuthorizedApiTestCase(APITestCase):
    def set_up(self, url) -> None:
        self.url = reverse(url)
        self.user_data = UserFactory()
        self.client.force_authenticate(user=self.user_data)
        return super().setUp()
