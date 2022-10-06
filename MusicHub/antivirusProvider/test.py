from rest_framework.test import APITestCase

from MusicHub.antivirusProvider.custom_exception import CustomAntiVirusException

from .service import AntivirusScan
from unittest.mock import patch

FILE_MALICIOUS = "File is malicius or suspicious, cannot upload it"
FILE_FAILED = "Failed to scan file, please try again later"


class TestAntivirusProvider(APITestCase):
    def setUp(self) -> None:
        self.antivirus = AntivirusScan()

    def mock_and_assert_raises_error(self, mock_sent_request, statuses, message):
        for status in statuses:
            mock_sent_request.return_value = {
                "scan_results": {
                    "scan_all_result_i": status,
                    "progress_percentage": 100,
                }
            }
            with self.assertRaises(CustomAntiVirusException):
                self.antivirus.scan_file_for_malicious_content("")

    @patch("MusicHub.antivirusProvider.service.AntivirusScan.sent_request")
    def test_no_threat_detected(self, mock_sent_request):
        mock_sent_request.return_value = {
            "scan_results": {"scan_all_result_i": 0, "progress_percentage": 100}
        }
        self.antivirus.scan_file_for_malicious_content("test")

    @patch("MusicHub.antivirusProvider.service.AntivirusScan.sent_request")
    def test_malicous_file_fail(self, mock_sent_request):

        self.mock_and_assert_raises_error(
            mock_sent_request, self.antivirus.bad_status, FILE_MALICIOUS
        )

    @patch("MusicHub.antivirusProvider.service.AntivirusScan.sent_request")
    def test_failed_upload_fail(self, mock_sent_request):

        self.mock_and_assert_raises_error(
            mock_sent_request, self.antivirus.failed_scan_status, FILE_FAILED
        )

    @patch("MusicHub.antivirusProvider.service.AntivirusScan.sent_request")
    def test_not_suported_or_other_fail(self, mock_sent_request):

        self.mock_and_assert_raises_error(
            mock_sent_request, [23], "Not supported media type"
        )

        self.mock_and_assert_raises_error(
            mock_sent_request, [55], "Unknown error during scanning file"
        )