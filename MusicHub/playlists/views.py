from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated

from .models import Playlist
from .serializers import PlaylistSerializer


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


class UpdatePlaylistView(UpdateAPIView):
    """
    Change the cover image for a playlist
    """

    queryset = Playlist.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer
    parser_class = MultiPartParser
    http_method_names = ["patch"]
