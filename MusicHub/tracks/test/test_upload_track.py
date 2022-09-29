from os.path import join

from ...config.settings import BASE_DIR
from ...users.test.base_test import AuthorizedApiTestCase


class TestUploadFile(AuthorizedApiTestCase):
    def setUp(self) -> None:
        self.set_up("upload-track")
        self.file_path = join(BASE_DIR.parent, "media", "tracks", "test\\")

    def load_file(self, filename, status_code):
        with open(f"{self.file_path}{filename}", "rb") as fp:
            response = self.client.post(path=self.url, data={"track": fp})

            self.assertEqual(response.status_code, status_code)

    def test_upload_file_success(self):
        self.load_file("test.mp3", 201)

    def test_upload_wrong_file_format(self):
        self.load_file("test.ogg", 400)

    def test_upload_to_big_file(self):
        self.load_file("file-to-big.wav", 400)

    def test_upload_wrong_name(self):
        self.load_file("wrong-name!_test.mp3", 400)
