from django.test import TestCase

from MusicHub.antivirusProvider.custom_exception import CustomAntiVirusException
from .service import AntivirusScan

FILE_MALICIOUS = "File is malicius or suspicious, cannot upload it"
FILE_FAILED = "Failed to scan file, please try again later"


class TestAntivirusProvider(TestCase):
    def setUp(self) -> None:
        self.antivirus = AntivirusScan()

    def check_result(self, result_scan_value, error_message):
        response = {"scan_results": {"scan_all_result_i": result_scan_value}}
        try:
            response = self.antivirus.check_result(
                response.get("scan_results").get("scan_all_result_i")
            )
        except CustomAntiVirusException as e:
            self.assertEqual(str(e), error_message)

    def test_no_threat_detected(self):
        response = {"scan_results": {"scan_all_result_i": 0}}

        try:
            self.antivirus.check_result(
                response.get("scan_results").get("scan_all_result_i")
            )
        except CustomAntiVirusException as e:
            self.fail()

    def test_malicous_file(self):
        self.check_result(1, FILE_MALICIOUS)

        self.check_result(2, FILE_MALICIOUS)

        self.check_result(18, FILE_MALICIOUS)

    def test_failed_upload(self):

        self.check_result(3, FILE_FAILED)
        self.check_result(10, FILE_FAILED)
        self.check_result(11, FILE_FAILED)
        self.check_result(19, FILE_FAILED)

    def test_not_suported_or_other(self):

        self.check_result(23, "Not supported media type")

        self.check_result(55, "Unknown error during scanning file")
