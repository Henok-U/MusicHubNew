from django.utils.datastructures import MultiValueDictKeyError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from MusicHub.users import custom_user_schema

from ...main.exception_handler import CustomUserException
from ..models import User
from ..serializers import AddChangePictureSerializer


class AddUpdateProfilePicture(GenericAPIView):
    """
    View responsible for adding or updating existing user profile picture.
    User must be authenticated in order to add or update picture.
    default relative path to picture is /media/users/avatar/example.jpg

    """

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            custom_user_schema.add_update_picture_headear,
            custom_user_schema.add_update_picture_body,
        ],
        responses=custom_user_schema.add_update_picture_response,
    )
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
        except (MultiValueDictKeyError, KeyError):
            raise CustomUserException("Please provide valid body arguments")
