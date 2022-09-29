from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from tinytag import TinyTag

from MusicHub.main.utils import format_to_minutes
from MusicHub.tracks.models import Track


class CreateTrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ["filename", "track", "public"]

    def validate_track(self, value):
        if value.size > 30000000:
            raise ValidationError("File cannot be bigger than 30 Mb")
        return value

    def create(self, validated_data):

        track = Track.objects.create(
            created_by=self.context.get("user"), **validated_data
        )
        track.track_length = TinyTag.get(track.track.path).duration
        track.save()
        return track


class ListTrackSerializer(ModelSerializer):
    playlist = serializers.PrimaryKeyRelatedField(
        many=False, read_only="True", default=None
    )
    # playlist = models.OneToOneField(Playlist, related_name='name')

    class Meta:
        model = Track
        fields = ["id", "filename", "track_length", "created_at", "public", "playlist"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "filename": instance.filename,
            "track_length": format_to_minutes(instance.track_length),
            "created_at": instance.created_at.strftime("%d:%M:%Y"),
            "public": instance.public,
            "playlist": None,  # fix later
        }
