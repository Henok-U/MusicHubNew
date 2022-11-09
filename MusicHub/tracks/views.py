from django.utils.decorators import method_decorator
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from MusicHub.main.swagger_parameters import TOKEN_PARAMETER, basic_response
from MusicHub.main.utils import LargeResultsSetPagination
from MusicHub.tracks import custom_track_schema
from MusicHub.tracks.models import Track
from MusicHub.tracks.serializers import CreateTrackSerializer, ListTrackSerializer


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
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
        manual_parameters=[TOKEN_PARAMETER],
        responses=basic_response("200", custom_track_schema.list_example, "400"),
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
        manual_parameters=[TOKEN_PARAMETER],
        responses=basic_response("200", "Track deleted successfully", "400"),
    ),
)
class DeleteOneTrackView(generics.DestroyAPIView):
    """
    View for deleting tracks owned by user
    provided id of track
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ListTrackSerializer
    queryset = Track.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Track deleted Successfull!"},
            status=status.HTTP_204_NO_CONTENT,
        )
