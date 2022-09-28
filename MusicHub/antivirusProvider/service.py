from time import sleep
from MusicHub.antivirusProvider.custom_exception import CustomAntiVirusException
from ..config.settings import Common
import requests
import json


class AntivirusScan:
    def __init__(self):
        self.file_url = "https://api.metadefender.com/v4/file/"
        self.post_headers = {
            "Content-Type": "application/octet-stream",
            "apikey": Common.ANTIVIRUS_API_KEY,
        }
        self.get_headers = {
            "apikey": Common.ANTIVIRUS_API_KEY,
            "x-file-metadata": "1",
        }
        self.bad_status = (
            1,  # "Infected/Known",
            2,  # "Suspicious",
            18,  # "Potentially Vulnerable File",
        )
        self.failed_scan_status = (
            3,  # "Failed To Scan",
            11,  # "Aborted",
            10,  # "Not Scanned / No scan results",
            19,  # "Canceled",
        )
        self.not_supported_status = 23  # "Filetype not supported"

    def scan_file_for_malicious_content(self, track):

        response = self.sent_request(self.post_headers, "post", track=track)

        response = self.sent_request(
            self.get_headers, "get", data_id=response.get("data_id")
        )
        while not response.get("scan_results").get("progress_percentage") == 100:
            sleep(1)
            response = self.sent_request(
                self.get_headers, "get", data_id=response.get("data_id")
            )
        self.check_result(response.get("scan_results").get("scan_all_result_i"))

    def sent_request(self, headers, request_type, track=None, data_id=None):
        try:
            if request_type == "get":
                return json.loads(
                    requests.get(f"{self.file_url}{data_id}", headers=headers).text
                )
            else:
                return json.loads(
                    requests.post(f"{self.file_url}", data=track, headers=headers).text
                )
        except Exception:
            raise CustomAntiVirusException(
                "Error during communicating with antivirus software"
            )

    def check_result(self, result):
        if result == 0:
            return
        if result in self.bad_status:
            raise CustomAntiVirusException(
                "File is malicius or suspicious, cannot upload it"
            )
        if result in self.failed_scan_status:
            raise CustomAntiVirusException(
                "Failed to scan file, please try again later"
            )
        if result == self.not_supported_status:
            raise CustomAntiVirusException("Not supported media type")

        raise CustomAntiVirusException("Unknown error during scanning file")
