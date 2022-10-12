import pytest
from .playlist_factory import PlaylistFactory
from django.urls import reverse

pytestmark = [pytest.mark.playlist, pytest.mark.django_db]


@pytest.fixture
def get_url():
    return reverse("list-own-playlist")


@pytest.mark.parametrize("number_of_playlists", [0, 5, 15])
def test_get_list_own_playlist_success(
    number_of_playlists, authorized_api_client, get_url, create_user
):
    """Get list of playlists for authorized user"""
    PlaylistFactory.create_batch(10)
    PlaylistFactory.create_batch(number_of_playlists, created_by=create_user)
    response = authorized_api_client.get(get_url)

    assert response.status_code == 200
    assert response.data.get("count") == number_of_playlists
