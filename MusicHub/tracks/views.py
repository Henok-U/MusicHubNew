from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from requests import request
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from MusicHub.main.utils import LargeResultsSetPagination
from MusicHub.tracks import custom_track_schema
from MusicHub.tracks.models import Track
from MusicHub.tracks.serializers import (
    AddTrackToPlaylistSerializer,
    CreateTrackSerializer,
    ListTrackSerializer,
)

from .custom_track_schema import TOKEN_PARAMETER
from drf_yasg.utils import no_body


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        auto_schema=custom_track_schema.CustomSwaggerAutoSchema,
        manual_parameters=[
            TOKEN_PARAMETER,
            custom_track_schema.track_file,
            custom_track_schema.is_public,
        ],
        request_body=no_body,
    ),
)
class UploadTrackView(CreateAPIView):
    """
    View for uploading new track by user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CreateTrackSerializer
    parser_classes = [MultiPartParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[custom_track_schema.TOKEN_PARAMETER],
        responses=custom_track_schema.basic_response(
            "200", custom_track_schema.list_example
        ),
    ),
)
class ListTracksView(generics.ListAPIView):
    """
    View for listing tracks owned by user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ListTrackSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        tracks = Track.objects.filter(created_by=self.request.user)
        return tracks.order_by("-created_at")


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        manual_parameters=[custom_track_schema.TOKEN_PARAMETER],
        responses=custom_track_schema.basic_response(
            "200", "Track deleted successfully"
        ),
    ),
)
class DeleteOneTrackView(generics.DestroyAPIView):
    """
    View for deleting tracks owned by user
    provided id of track
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ListTrackSerializer

    def get_queryset(self):
        track = Track.objects.all()
        return track

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Track deleted Successfull!"},
            status=status.HTTP_204_NO_CONTENT,
        )


class AddTrackToPlaylist(UpdateAPIView):
    """View for adding user track to his playlist"""

    permission_classes = [IsAuthenticated]
    serializer_class = AddTrackToPlaylistSerializer
    http_method_names = ["patch"]

    def get_queryset(self):
        """Ensures that user can only add tracks that belong to him"""
        return Track.objects.filter(created_by=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context
