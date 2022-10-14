from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from MusicHub.main.exception_handler import CustomException

from .models import Playlist
from .serializers import PlaylistSerializer, ListPlaylistSerializer
from ..main.utils import LargeResultsSetPagination
from .custom_playlist_schema import TOKEN_PARAMETER, optional_track_id


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


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[TOKEN_PARAMETER, optional_track_id]
    ),
)
class ListOwnPlaylistView(ListAPIView):
    """
    View to see list of playlists created by authorized user
    only authorized user can see his own playlist
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ListPlaylistSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        track_id = self.request.query_params.get("track")
        query = Playlist.objects.filter(created_by=self.request.user).order_by(
            "-created_at"
        )
        if track_id:
            try:
                return query.exclude(track=track_id)
            except Exception as e:
                raise CustomException(str(e))
        else:
            return query
