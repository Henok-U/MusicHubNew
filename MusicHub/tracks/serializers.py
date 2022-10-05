from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from tinytag import TinyTag

from MusicHub.main.utils import format_sec_to_mins
from MusicHub.tracks.models import Track

from .constants import FORMATED_DATE, MAX_FILE_SIZE


class CreateTrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ["filename", "file", "is_public"]

    def validate_track(self, value):
        if value.size > MAX_FILE_SIZE:
            raise ValidationError("File cannot be bigger than 30 Mb")
        return value

    def create(self, validated_data):

        track = Track.objects.create(
            created_by=self.context.get("user"), **validated_data
        )
        track.track_length = TinyTag.get(track.file.path).duration
        track.save()
        return track


class ListTrackSerializer(ModelSerializer):
    playlist = serializers.PrimaryKeyRelatedField(
        many=False, read_only="True", default=None
    )

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
            "playlist": None,
        }
