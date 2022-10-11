from uuid import uuid4
from rest_framework import serializers

from MusicHub.tracks.constants import FORMATED_DATE

from .models import Playlist
from .services import validate_picture
from ..main.utils import rename_image_to_random


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["id", "name", "is_public", "playlist_image"]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def validate_playlist_image(self, obj):
        validate_picture(obj)
        return obj

    def create(self, validated_data):
        playlist = Playlist.objects.create(
            created_by=self.context.get("user"), **validated_data
        )
        return playlist

    def save(self, **kwargs):
        """
        override save() method to rename cover image of playlist
        to a randomly generated name
        """
        image_name = self.initial_data["playlist_image"].name
        self.initial_data["playlist_image"].name = rename_image_to_random(image_name)

        return super().save(**kwargs)


class ListPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["name", "likes", "is_public", "created_at", "playlist_image"]

    def to_representation(self, instance):
        instance.created_at = instance.created_at.strftime(FORMATED_DATE)
        return super().to_representation(instance)
