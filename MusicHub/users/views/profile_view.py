from functools import partial
from signal import raise_signal
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import AddChangePictureSerializer
from ..models import User
from ...main.exception_handler import CustomUserException
from django.utils.datastructures import MultiValueDictKeyError


class AddUpdateProfilePicture(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AddChangePictureSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.user.email)
            serializer = AddChangePictureSerializer(
                user, data={"profile_avatar": request.data["picture"]}, partial=True
            )
            serializer.is_valid(raise_exception=True)
            if not user.profile_avatar == "":
                user.profile_avatar.delete()
            serializer.save()
            return Response(status=200, data="Picture added successfully")

        except User.DoesNotExist:
            raise CustomUserException("Could not find user with given credentials")
        except MultiValueDictKeyError:
            raise CustomUserException("Please provide valid body arguments")
