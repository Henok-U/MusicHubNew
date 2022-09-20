from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import GenericAPIView

from MusicHub.users.models import User
from MusicHub.users.serializers import ProfileSerializer


class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = ProfileSerializer(request.user)
        return Response(data=serializer.data)

    def patch(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        data = {
            "first_name": request.data["first_name"],
            "last_name": request.data["last_name"],
        }
        serializer = ProfileSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        content = {"message": "Profile Updated successfully"}
        return Response(data=content)
