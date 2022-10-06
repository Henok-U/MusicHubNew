from rest_framework import status

from MusicHub.users.models import User
from MusicHub.users.test.base_test import AuthorizedApiTestCase


class TestProfileView(AuthorizedApiTestCase):
    def setUp(self):
        self.set_up("profile")

    def test_successful_profile_view_and_edit(self):
        # get the profile
        self.get_and_assert_equal_status_code(status_code=status.HTTP_200_OK)

        # user changes profile
        data = {
            "first_name": "Sam",
            "last_name": "Harris",
        }
        self.patch_and_assert_equal_status_code(
            data=data, status_code=status.HTTP_200_OK
        )

        # get the user's data
        self.user_data = User.objects.filter(first_name="Sam").get()
        self.client.force_authenticate(self.user_data)

        # get updated profile
        self.get_and_assert_equal_status_code(status_code=status.HTTP_200_OK)
