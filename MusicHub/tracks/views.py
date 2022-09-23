from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CreateTrackSerializer


class UploadTrackView(CreateAPIView):
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
