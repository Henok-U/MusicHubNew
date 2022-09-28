from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Track
from tinytag import TinyTag

MAX_FILE_SIZE = 30_000_000  # values in bytes, max 30Mb


class CreateTrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ["filename", "track"]

    def validate_track(self, value):
        if value.size > MAX_FILE_SIZE:
            raise ValidationError("File cannot be bigger than 30 Mb")
        return value

    def create(self, validated_data):

        track = Track.objects.create(
            created_by=self.context.get("user"), **validated_data
        )
        track.track_length = TinyTag.get(track.track.path).duration
        track.save()
        return track
