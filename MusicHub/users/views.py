from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    ResetPasswordSerializer,
    ResetPasswordEmailSerializer,
)
from ..main.exception_handler import CustomUserException, custom_exception_handler
from MusicHub.main.utils import check_code_for_verification
from authemail.models import SignupCode, PasswordResetCode

from authemail.views import SignupVerify
from MusicHub.main.utils import verification_email, reset_password_email
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.datastructures import MultiValueDictKeyError


class CreateUserView(CreateAPIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        queryset = User.objects.filter(email=request.data["email"])

        if queryset.exists():
            if queryset.get().is_verified:
                raise CustomUserException("Provided email address is already in use")
            else:
                token_date = SignupCode.objects.get(user=queryset.get()).created_at
                diff = (timezone.now() - token_date).days * 24

                if SignupCode.objects.filter(user=queryset.get()) and diff <= 24:
                    return Response(status=400, data="Please verify your email")
                else:
                    verification_email(queryset.get(), request)
        if not "confirm_password" in request.data.keys():
            raise CustomUserException("Confirm password field is required")
        if not request.data["password"] == request.data["confirm_password"]:
            raise CustomUserException("Passwords does not match")

        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        model_serializer = UserSerializer(data=serializer.data)
        model_serializer.is_valid(raise_exception=True)
        user = model_serializer.save()
        try:
            verification_email(user, request)
        except Exception:
            raise CustomUserException("Error during sending email.")

        return Response(status=200, data=model_serializer.data)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                description="Successful verification\nGET api/accounts/signup/verify/?code=<token>",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class CreateUserVerify(SignupVerify):
    def get(self, request, format=None):
        code = request.GET.get("code", "")
        verification_code = check_code_for_verification(code, SignupCode)
        try:

            verification_code.user.is_verified = True
            verification_code.user.save()
            verification_code.delete()
        except Exception:
            raise custom_exception_handler("Unable to verify user")
        return Response(data="Email address verified.", status=200)


class RecoverPassword(GenericAPIView):
    """
    View to handle sending email with reset password link and
    changing password to a new one

    """

    queryset = User.objects.get_queryset_verified()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ResetPasswordEmailSerializer
        elif self.request.method == "PUT":
            return ResetPasswordSerializer

    @swagger_auto_schema(responses={200: "Message"})
    def post(self, request, format=None):
        """
        Sends email with link to reset password for given email address
        """
        try:
            serializer = ResetPasswordEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.queryset.get(email=request.data["email"])
            reset_password_email(user, request)
        except User.DoesNotExist:
            raise CustomUserException("Account with given email does not exists")
        return Response(
            status=200, data="Reset link was sucessfully send to given address email"
        )

    @swagger_auto_schema(responses={200: "Message"})
    def put(self, request, format=None):
        """
        Changes password for given user in reset code
        """
        try:
            code = request.query_params["code"]
        except MultiValueDictKeyError:
            raise CustomUserException("code is needed")
        reset_code = check_code_for_verification(code, PasswordResetCode)

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.data["password"] == request.data["confirm_password"]:
            raise CustomUserException("Passwords does not match")

        try:
            user = reset_code.user
            user.set_password(request.data["password"])
            user.save()
            reset_code.delete()
        except Exception:
            raise CustomUserException("Unable to change user password")

        return Response(status=200, data="Password was successfully changed")
