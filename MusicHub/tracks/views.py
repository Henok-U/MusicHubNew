from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from .custom_track_schema import TOKEN_PARAMETER
from drf_yasg.utils import swagger_auto_schema
from .serializers import CreateTrackSerializer


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        manual_parameters=[TOKEN_PARAMETER],
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
