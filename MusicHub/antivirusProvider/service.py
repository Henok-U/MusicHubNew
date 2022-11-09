import json
from time import sleep

import requests

from MusicHub.antivirusProvider.custom_exception import CustomAntiVirusException

from ..config.settings import Common
from .constants import (
    ANTIVIRUS_BASE_URL,
    CHECK_PROGRESS_DELAY_SECONDS,
    PROGRES_PERCENTAGE,
    AntivirusStatuses,
)


class AntivirusScan:
    def __init__(self, filename):
        self.file_url = ANTIVIRUS_BASE_URL
        self.post_headers = {
            "Content-Type": "application/octet-stream",
            "apikey": Common.ANTIVIRUS_API_KEY,
            "filename": filename,
        }
        self.get_headers = {
            "apikey": Common.ANTIVIRUS_API_KEY,
            "x-file-metadata": "0",
        }
        self.bad_status = (
            AntivirusStatuses.INFECTED,
            AntivirusStatuses.SUSPICIOUS,
            AntivirusStatuses.POTENTIALY_VULNERABLE_FILE,
        )
        self.failed_scan_status = (
            AntivirusStatuses.FAILED_TO_SCAN,
            AntivirusStatuses.ABORTED,
            AntivirusStatuses.NOT_SCANNED,
            AntivirusStatuses.CANCELED,
        )
        self.not_supported_status = AntivirusStatuses.FILETYPE_NOT_SUPPORTED

    def scan_file_for_malicious_content(self, track):

        response = self.sent_request(self.post_headers, "post", file=track)

        response = self.wait_for_progress_finished(response)

        self.check_result(response.get("scan_results").get("scan_all_result_i"))

    def wait_for_progress_finished(self, response):
        response = self.sent_request(
            self.get_headers, "get", data_id=response.get("data_id")
        )
        while (
            not response.get("scan_results").get("progress_percentage")
            == PROGRES_PERCENTAGE
        ):
            sleep(CHECK_PROGRESS_DELAY_SECONDS)
            response = self.sent_request(
                self.get_headers, "get", data_id=response.get("data_id")
            )
        return response

    def sent_request(self, headers, request_type, file=None, data_id=None):
        try:
            if request_type == "get":
                return json.loads(
                    requests.get(f"{self.file_url}{data_id}", headers=headers).text
                )
            else:
                return json.loads(
                    requests.post(f"{self.file_url}", data=file, headers=headers).text
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
