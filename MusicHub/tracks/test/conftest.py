import pytest
from rest_framework.test import APIClient
from MusicHub.users.test.user_factory import UserFactory


@pytest.fixture
def create_user():
    return UserFactory()


@pytest.fixture
def authorized_api_client(create_user):
    api_client = APIClient()
    api_client.force_authenticate(user=create_user)
    return api_client
