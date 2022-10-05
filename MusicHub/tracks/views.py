from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from MusicHub.main.utils import LargeResultsSetPagination
from MusicHub.tracks import custom_track_schema
from MusicHub.tracks.models import Track
from MusicHub.tracks.serializers import (
    CreateTrackSerializer,
    ListTrackSerializer,
)


class UploadTrackView(generics.CreateAPIView):
    """
    View for uploading new track by user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CreateTrackSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateTrackSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201, data=serializer.data)


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

    def get_queryset(self):
        tracks = Track.objects.filter(created_by=self.request.user)
        return tracks.order_by("-created_at")

    permission_classes = [IsAuthenticated]
    serializer_class = ListTrackSerializer
    pagination_class = LargeResultsSetPagination


class DeleteOneTrackView(generics.DestroyAPIView):
    """
    View for deleting tracks owned by user
    provided id of track
    """

    def get_queryset(self):
        track = Track.objects.all()
        return track

    permission_classes = [IsAuthenticated]
    serializer_class = ListTrackSerializer

    @swagger_auto_schema(
        manual_parameters=[
            custom_track_schema.TOKEN_PARAMETER,
        ],
        responses=custom_track_schema.basic_response(
            "200", "Track deleted successfully"
        ),
    )
    def delete(self, request, *args, **kwargs):
        try:
            track = self.get_object()
            self.perform_destroy(track)
            return Response(
                {"message": "Track deleted Successfull!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Track.DoesNotExist:
            return Response(
                {"message": "Unable to delete, Invalid track id!"},
                status=status.HTTP_404_NOT_FOUND,
            )