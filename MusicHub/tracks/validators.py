from rest_framework.serializers import ValidationError

from ..antivirusProvider.service import AntivirusScan
from ..main.constants import MAX_FILE_SIZE_IN_MB


def validate_track(data):
    if data.size >= MAX_FILE_SIZE_IN_MB:
        raise ValidationError("File cannot be bigger than 30 Mb")
    scanner = AntivirusScan(data.name)
    scanner.scan_file_for_malicious_content(data)
