from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.parsers import MultiPartParser
from MusicHub.main.exception_handler import (
    CustomUserException,
    custom_exception_handler,
)
from MusicHub.users import custom_user_schema
from MusicHub.users.models import User
from MusicHub.users.serializers import (
    ChangePasswordSerializer,
    ProfileSerializer,
    AddChangePictureSerializer,
)


class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    @swagger_auto_schema(
        manual_parameters=custom_user_schema.authorization_token,
        responses=custom_user_schema.profile_get_response,
    )
    def get(self, request, *args, **kwargs):
        try:
            serializer = ProfileSerializer(request.user)
        except ValidationError:
            raise custom_exception_handler
        return Response(data=serializer.data)

    @swagger_auto_schema(
        manual_parameters=custom_user_schema.authorization_token,
        request_body=custom_user_schema.profile_update_request,
        responses=custom_user_schema.profile_update_responses,
    )
    def patch(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        data = {
            "first_name": request.data["first_name"],
            "last_name": request.data["last_name"],
        }
        try:
            serializer = ProfileSerializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError:
            raise custom_exception_handler

        content = {"message": "Profile Updated successfully"}
        return Response(data=content)


class ChangePassword(GenericAPIView):
    """
    View allowing authorized user to change their password
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=custom_user_schema.authorization_token,
        request_body=ChangePasswordSerializer,
        responses=custom_user_schema.reset_password_returns,
    )
    def patch(self, request, *args, **kwargs):
        try:

            user = User.objects.get(email=request.user.email)
            serializer = ChangePasswordSerializer(
                user, data=request.data, context={"user": user}, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=200, data="Password changed successfully")
        except (MultiValueDictKeyError, KeyError):
            raise CustomUserException("Please provide valid data")


class AddUpdateProfilePicture(GenericAPIView):
    """
    View responsible for adding or updating existing user profile picture.
    User must be authenticated in order to add or update picture.
    default relative path to picture is /media/users/avatar/example.jpg

    """

    def get_serializer(self, *args, **kwargs):
        pass

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
