from mutagen.mp3 import MP3
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Track

MAX_FILE_SIZE = 30_000_000  # values in bytes, max 30Mb


class CreateTrackSerializer(ModelSerializer):
    class Meta:

        model = Track
        fields = ["filename", "id", "track", "public"]
        extra_kwargs = {"id": {"read_only": True}}

    def validate_track(self, value):
        if value.size >= MAX_FILE_SIZE:
            raise ValidationError("File cannot be bigger than 30 Mb")
        return value

    def create(self, validated_data):
        validated_data["track_length"] = int(
            MP3(validated_data.get("track")).info.length
        )
        track = Track.objects.create(
            created_by=self.context.get("user"), **validated_data
        )
        return track
