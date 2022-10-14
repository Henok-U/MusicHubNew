import pytest
from django.urls import reverse
from MusicHub.playlists.test.playlist_factory import PlaylistFactory
from MusicHub.tracks.test.track_factory import TrackFactory
from MusicHub.users.test.user_factory import UserFactory
from MusicHub.tracks.models import Track

pytestmark = [pytest.mark.tracks, pytest.mark.django_db]


def set_up_data_and_url(*args, **kwargs):
    track = TrackFactory(*args, **kwargs)
    playlist = PlaylistFactory(*args, **kwargs)
    url = reverse("add-track-to-playlist", kwargs={"pk": track.id})
    return track, playlist, url


def get_track_from_db_and_assert_equal(track_id, **kwargs):
    track_from_db = Track.objects.get(id=track_id)
    for key, value in kwargs.items():

        assert track_from_db.__dict__[key] == value


def add_track_to_playlist(authorized_api_client, create_user, **kwargs):
    track, playlist, url = set_up_data_and_url(created_by=create_user, **kwargs)
    if "is_public" in kwargs.keys():
        track.is_public = not kwargs["is_public"]
        track.save()

    response = authorized_api_client.patch(url, data={"playlist": playlist.name})

    assert response.status_code == 200
    if ("likes" in kwargs.keys()) and (
        not playlist.is_public
    ):  # If the playlist is private, then likes will be removed
        kwargs.pop("likes")
    get_track_from_db_and_assert_equal(track.id, **kwargs)

    return track, playlist, response


def test_add_track_to_playlist_success(authorized_api_client, create_user):
    """Succesfull adding track to playlist"""

    add_track_to_playlist(authorized_api_client, create_user)


def test_add_private_track_to_public_playlist(authorized_api_client, create_user):
    """Succesfull adding track to playlist
    Track changes his public status to playlist status"""
    add_track_to_playlist(authorized_api_client, create_user, is_public=True)


def test_add_public_track_to_private_playlist(authorized_api_client, create_user):
    """Succesfull adding track to playlist
    Track changes his public status to playlist status"""
    add_track_to_playlist(authorized_api_client, create_user, is_public=False)


def test_add_public_track_to_private_playlist_and_remove_likes(
    authorized_api_client, create_user
):
    """Succesfull adding track to playlist
    After moving public track with likes to private playlist, likes are cleared"""
    liked_users = UserFactory.create_batch(10)
    track, playlist, response = add_track_to_playlist(
        authorized_api_client,
        create_user,
        is_public=False,
        likes=liked_users,
    )

    assert Track.objects.aggregate_likes(track_likes=track) == 0


def test_add_track_to_playlist_wrong_track(authorized_api_client, create_user):
    """try to add to playlist track with does not exists"""
    playlist = PlaylistFactory(created_by=create_user)
    url = reverse("add-track-to-playlist", kwargs={"pk": "notvalid"})
    response = authorized_api_client.patch(url, data={"playlist": playlist.name})

    assert response.status_code == 404


def test_add_track_to_playlist_wrong_playlist_name(authorized_api_client, create_user):
    """try to add track to playlist with does not exists"""
    track = TrackFactory(created_by=create_user)
    url = reverse("add-track-to-playlist", kwargs={"pk": track.id})
    response = authorized_api_client.patch(url, data={"playlist": "not_valid_name"})

    assert response.status_code == 400


def test_add_track_to_not_user_playlist(authorized_api_client, create_user):
    """try to add track to playlist that does not belong to user"""
    track, playlist, url = set_up_data_and_url(created_by=create_user)
    not_user_playlist = PlaylistFactory()
    response = authorized_api_client.patch(
        url, data={"playlist": not_user_playlist.name}
    )

    assert response.status_code == 400
