from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from MusicHub.playlists.custom_playlist_schema import TOKEN_PARAMETER

from .models import Playlist
from .serializers import PlaylistSerializer


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(manual_parameters=[TOKEN_PARAMETER]),
)
class CreatePlaylistView(CreateAPIView):
    """
    Create a new Playlist
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer
    parser_class = MultiPartParser

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context


@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(manual_parameters=[TOKEN_PARAMETER]),
)
class UpdatePlaylistView(UpdateAPIView):
    """
    Change the cover image for a playlist
    """

    queryset = Playlist.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer
    parser_class = MultiPartParser
    http_method_names = ["patch"]
