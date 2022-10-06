from rest_framework.serializers import ModelSerializer
from django.utils.decorators import method_decorator
from ..main.utils import exclude_fields_from_swagger_schema
from .track_service import get_track_length, validate_track
from .models import Track


@method_decorator(
    name="get_fields", decorator=exclude_fields_from_swagger_schema(["filename"])
)
class CreateTrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ["filename", "track"]

    def to_internal_value(self, data):
        data["filename"] = data.get("track").name
        data["track_length"] = get_track_length(data.get("track"))
        return super().to_internal_value(data)

    def validate_track(self, value):
        validate_track(value)
        return value

    def create(self, validated_data):
        track = Track.objects.create(
            created_by=self.context.get("user"), **validated_data
        )
        return track
