from os.path import join

from ...config.settings import BASE_DIR
from ...users.test.base_test import AuthorizedApiTestCase
from ..models import Track


class TestUploadFile(AuthorizedApiTestCase):
    def setUp(self) -> None:
        self.set_up("upload-track")
        self.file_path = join(BASE_DIR.parent, "media", "tracks", "test\\")

    def load_file(self, filename, status_code):
        with open(f"{self.file_path}{filename}", "rb") as fp:
            response = self.client.post(
                path=self.url, data={"track": fp, "public": False}
            )

            self.assertEqual(response.status_code, status_code)
            return response

    def test_upload_file_success(self):
        response = self.load_file("test.mp3", 201)

        track = Track.objects.get(id=response.data.get("id"))
        self.assertEqual(track.public, False)

    def test_upload_wrong_file_format(self):
        self.load_file("test.ogg", 400)

    def test_upload_to_big_file(self):
        self.load_file("file-to-big.wav", 400)

    def test_upload_wrong_name(self):
        self.load_file("wrong-name!_test.mp3", 400)
