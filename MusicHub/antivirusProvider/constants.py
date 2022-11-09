from enum import Enum


class AntivirusStatuses(Enum):
    INFECTED = 1
    SUSPICIOUS = 2
    POTENTIALY_VULNERABLE_FILE = 18
    FAILED_TO_SCAN = 3
    ABORTED = 11
    NOT_SCANNED = 10
    CANCELED = 19
    FILETYPE_NOT_SUPPORTED = 23


CHECK_PROGRESS_DELAY_SECONDS = 1
PROGRES_PERCENTAGE = 100
ANTIVIRUS_BASE_URL = "https://api.metadefender.com/v4/file/"
