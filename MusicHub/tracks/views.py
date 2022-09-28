from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CreateTrackSerializer
from ..antivirusProvider.service import AntivirusScan
from .track_service import get_filename_from_track


class UploadTrackView(CreateAPIView):
    """
    View for uploading new track by user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CreateTrackSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateTrackSerializer(
            data=get_filename_from_track(request), context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)

        scanner = AntivirusScan()
        scanner.scan_file_for_malicious_content(request.data.get("track"))

        serializer.save()
        return Response(status=201, data=serializer.data)
