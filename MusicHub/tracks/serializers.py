from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from MusicHub.playlists.models import Playlist
from MusicHub.tracks.validators import is_user_owner_of_obj

from ..main.utils import format_sec_to_mins
from .constants import FORMATED_DATE
from .track_service import (
    get_track_length,
    validate_track,
    remove_from_liked_when_set_to_private,
)
from .models import Track


class CreateTrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ["filename", "id", "track_length", "file", "is_public"]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def to_internal_value(self, data):
        data["filename"] = data.get("file").name
        data["track_length"] = get_track_length(data.get("file"))
        return super().to_internal_value(data)

    def validate_file(self, value):
        validate_track(value)
        return value

    def create(self, validated_data):
        track = Track.objects.create(
            created_by=self.context.get("user"), **validated_data
        )
        return track


class ListTrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = [
            "id",
            "filename",
            "track_length",
            "created_at",
            "is_public",
            "playlist",
        ]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "filename": instance.filename,
            "track_length": format_sec_to_mins(instance.track_length),
            "created_at": instance.created_at.strftime(FORMATED_DATE),
            "is_public": instance.is_public,
            "playlist": instance.playlist_id,
        }


class AddTrackToPlaylistSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ["playlist"]

    def validate_playlist(self, value):
        is_user_owner_of_obj(self.context.get("user"), value)
        return value

    def update(self, instance, validated_data):
        validated_data["is_public"] = validated_data["playlist"].is_public
        remove_from_liked_when_set_to_private(instance, validated_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return {"message": f"track added successfuly to playlist: {instance.playlist}"}
