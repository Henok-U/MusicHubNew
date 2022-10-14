from ..antivirusProvider.service import AntivirusScan
from ..main.constants import MAX_FILE_SIZE_IN_MB
from ..main.validators import validate_files


def validate_track(data):
    validate_files(data, MAX_FILE_SIZE_IN_MB)
    scanner = AntivirusScan(data.name)
    scanner.scan_file_for_malicious_content(data)
