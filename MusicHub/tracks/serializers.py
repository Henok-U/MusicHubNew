from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..main.constants import FORMATED_DATE
from ..main.utils import format_sec_to_mins
from .models import Track
from .track_service import get_track_length
from .validators import validate_track


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
