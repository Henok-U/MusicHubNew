from mutagen import mp3, wave, aac
from ..antivirusProvider.service import AntivirusScan
from ..antivirusProvider.service import AntivirusScan
from rest_framework.serializers import ValidationError
from .constants import MAX_FILE_SIZE_IN_MB


def get_track_length(file):
    # TODO rafactor this
    if file.name.split(".")[-1] == ".mp3":
        return int(mp3.MP3(file).info.length)
    if file.name.split(".")[-1] == ".wav":
        return int(wave.WAVE(file).info.length)
    if file.name.split(".")[-1] == ".aac":
        return int(aac.AAC(file).info.length)


def validate_track(data):
    scanner = AntivirusScan()
    scanner.scan_file_for_malicious_content(data)
    if data.size >= MAX_FILE_SIZE_IN_MB:
        raise ValidationError("File cannot be bigger than 30 Mb")
