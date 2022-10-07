from rest_framework import serializers

from .models import Playlist
from .services import validate_picture


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["name", "is_public", "playlist_image"]

    playlist_image = serializers.ImageField(validators=[validate_picture])
