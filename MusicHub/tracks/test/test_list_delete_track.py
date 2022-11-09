from rest_framework import status

from MusicHub.tracks.test.test_utils import delete_generated_files_testing_tracks
from MusicHub.tracks.test.track_factory import TrackFactory
from MusicHub.users.test.base_test import AuthorizedApiTestCase


class TestViewDeleteTrack(AuthorizedApiTestCase):
    def setUp(self):
        self.set_up("list-track")
        self.data = TrackFactory(created_by=self.user_data)

        delete_generated_files_testing_tracks(self.user_data.email)

    def test_list_tracks(self):
        self.get_and_assert_equal_status_code(status.HTTP_200_OK)

    def test_delete_track_invalid_pk(self):
        self.delete_and_assert_equal_status_code(
            "delete-track",
            "234234-invalid-pk022",
            status.HTTP_404_NOT_FOUND,
        )

    def test_delete_track_valid_pk(self):
        self.delete_and_assert_equal_status_code(
            "delete-track",
            self.data.pk,
            status.HTTP_204_NO_CONTENT,
        )
