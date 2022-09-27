from email.policy import default
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from .models import Track
from tinytag import TinyTag


class CreateTrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ["filename", "track"]

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
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    playlist = serializers.PrimaryKeyRelatedField(
        many=False, read_only="True", default=None
    )
    # playlist = models.OneToOneField(User, related_name='profile')

    class Meta:
        model = Track
        fields = ["id", "filename", "track_length", "created_at", "public", "playlist"]
