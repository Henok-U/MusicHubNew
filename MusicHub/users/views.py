from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from .models import User
from .serializers import CreateUserSerializer
from ..main.exception_handler import CustomUserException


class CreateUserView(CreateAPIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):

        queryset = User.objects.filter(email=request.data["email"])
        if queryset.exists():
            raise CustomUserException("Provided email address is already in use")
        if not "confirm_password" in request.data.keys():
            raise CustomUserException("Confirm password field is required")
        if not request.data["password"] == request.data["confirm_password"]:
            raise CustomUserException("Passwords does not match")

        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200, data=serializer.data)
