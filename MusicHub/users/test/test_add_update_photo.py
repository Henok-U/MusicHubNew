import os
from os.path import join
from pathlib import Path

from ..models import User
from .base_test import AuthorizedApiTestCase


class TestUserRegistrationAPIView(AuthorizedApiTestCase):
    def setUp(self):
        self.set_up("upload-photo")
        self.picture = Path(__file__).resolve().parent.parent.parent
        self.picture = join(os.path.dirname(self.picture), "media/users/avatar/")

    def load_upload_and_get_picture(self, filename, status_code):
        with open(f"{self.picture}{filename}", "rb") as fp:
            response = self.client.patch(path=self.url, data={"profile_avatar": fp})

            self.assertEqual(response.status_code, status_code)
            user = User.objects.get(email=self.user_data.email)
            return user.profile_avatar

    def test_add_and_update_photo_success(self):

        old_picture = self.load_upload_and_get_picture("test.jpg", 200)
        new_picture = self.load_upload_and_get_picture("test2.jpg", 200)
        self.assertNotEqual(old_picture.name, new_picture.name)

        User.objects.get(email=self.user_data.email).profile_avatar.delete()

    def test_add_invalid_photo_format_fail(self):

        self.load_upload_and_get_picture("image.jfif", 400)

    def test_add_picture_too_big_fail(self):

        self.load_upload_and_get_picture("testtt.jpg", 400)

    def test_add_picuture_no_body_arguments(self):

        response = self.client.patch(path=self.url, data={"profile_avatar": ""})
        self.assertEqual(response.status_code, 400)
