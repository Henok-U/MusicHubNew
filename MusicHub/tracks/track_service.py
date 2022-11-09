from mutagen import aac, mp3, wave


def get_track_length(file):
    filename = file.name.split(".")[-1]
    if filename == "mp3":
        return int(mp3.MP3(file).info.length)
    if filename == "wav":
        return int(wave.WAVE(file).info.length)
    if filename == "aac":
        return int(aac.AAC(file).info.length)
