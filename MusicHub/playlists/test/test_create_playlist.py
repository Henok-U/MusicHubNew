from operator import is_
from re import A
from urllib import response
import pytest
from django.urls import reverse
from rest_framework import status

from MusicHub.playlists.test.conftest import authorized_api_client

pytestmark = pytest.mark.django_db


class TestPlaylistCreateView:
    def post_and_assert(self, authorized_api_client, status_code, **kwargs):
        url = reverse("create-playlist")
        response = authorized_api_client.post(url, kwargs)
        assert response.status_code == status_code

    @pytest.mark.parametrize("name", ["Playlist 1", "Playlist 2", "Playlist 3"])
    def test_create_playlist_with_valid_names(self, authorized_api_client, name):
        self.post_and_assert(
            authorized_api_client=authorized_api_client,
            status_code=status.HTTP_201_CREATED,
            name=name,
            is_public="True",
        )

    @pytest.mark.parametrize("name", ["Playlist&1", "Playlist_2", "Playlist33#$3"])
    def test_create_playlist_with_invalid_names(self, authorized_api_client, name):
        self.post_and_assert(
            authorized_api_client=authorized_api_client,
            status_code=status.HTTP_400_BAD_REQUEST,
            name=name,
            is_public="True",
        )

    def test_fail_create_already_created_playlist(
        self, authorized_api_client, create_playlist
    ):
        self.post_and_assert(
            authorized_api_client=authorized_api_client,
            status_code=status.HTTP_400_BAD_REQUEST,
            name=create_playlist.name,
            is_public=create_playlist.is_public,
        )
