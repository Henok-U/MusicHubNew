from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *

from MusicHub.main.exception_handler import (
    CustomUserException,
    custom_exception_handler,
)
from MusicHub.users import custom_user_schema
from MusicHub.users.models import User
from MusicHub.users.serializers import ChangePasswordSerializer, ProfileSerializer


class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    @swagger_auto_schema(
        manual_parameters=custom_user_schema.profile_parameters,
        responses=custom_user_schema.profile_get_response,
    )
    def get(self, request, *args, **kwargs):
        try:
            serializer = ProfileSerializer(request.user)
        except ValidationError:
            raise custom_exception_handler
        return Response(data=serializer.data)

    @swagger_auto_schema(
        manual_parameters=custom_user_schema.profile_parameters,
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
