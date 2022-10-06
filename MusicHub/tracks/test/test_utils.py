import os
import shutil

from MusicHub.config.settings import BASE_DIR


def delete_generated_files_testing_tracks(email):
    user_track_folder_name = email.split("@")[0]
    tracks_path = os.path.join(
        os.path.dirname(BASE_DIR),
        "media",
        "tracks",
        user_track_folder_name,
    )
    shutil.rmtree(tracks_path)
