from urllib import response
import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from ..models import Playlist
from ...users.models import User


class TestPlaylistView:
    @pytest.mark.django_db
    def test_playlist_create(*args):
        me = User.objects.create(
            email="test@example.com", password="abcABC123", is_verified=True
        )
        Playlist.objects.create(name="Test Playlist", is_public=False, created_by=me)

        assert Playlist.objects.count() == 1

    @pytest.mark.django_db
    def test_unauthorized(client):
        url = reverse("create-playlist")
        response = client.post(url)
        print(response.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
