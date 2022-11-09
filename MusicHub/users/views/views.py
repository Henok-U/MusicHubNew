from authemail.models import PasswordResetCode, SignupCode
from authemail.views import SignupVerify
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.authtoken.models import Token as SigninToken
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from social_core.exceptions import AuthForbidden
from social_django.utils import psa

from MusicHub.main import swagger_parameters

from ...main.exception_handler import CustomUserException
from .. import custom_user_schema
from ..models import User
from ..serializers import (
    ResetPasswordEmailSerializer,
    ResetPasswordSerializer,
    SigninSerializer,
    SignupSerializer,
    SocialAuthSerializer,
)
from ..user_service import (
    check_code_for_verification,
    check_user_sign_up,
    delete_used_token,
    reset_password_email,
)


@method_decorator(
    name="post",
    decorator=[
        check_user_sign_up,
        swagger_auto_schema(
            responses=swagger_parameters.basic_response(
                201,
                {
                    "id": "string",
                    "email": "string",
                    "first_name": "string",
                    "last_name": "string",
                },
                400,
            ),
        ),
    ],
)
class SignUpView(CreateAPIView):
    """
    View for signing up user
    """

    serializer_class = SignupSerializer

    def get_queryset(self):
        return User.objects.filter(email=self.request.data.get("email"))


class SignUpVerifyView(SignupVerify):
    @swagger_auto_schema(
        manual_parameters=custom_user_schema.signup_verify_parameters,
        responses=swagger_parameters.basic_response(
            200, {"message": "Email address verified"}, 400
        ),
    )
    def get(self, request, format=None):

        code = request.query_params.get("code")
        verification_code = check_code_for_verification(code, SignupCode)
        verification_code.user.is_verified = True
        verification_code.user.save()
        verification_code.delete()
        return Response(data="Email address verified.", status=200)


class SignInView(GenericAPIView):

    serializer_class = SigninSerializer

    @swagger_auto_schema(
        responses=swagger_parameters.basic_response(200, {"token": "token"}, 401),
    )
    def post(self, request, *args, **kwargs):
        serializer = SigninSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                email=serializer.data["email"], password=serializer.data["password"]
            )

            if user:
                if user.is_verified:
                    if user.is_active:
                        token, created = SigninToken.objects.get_or_create(user=user)
                        content = {"token": token.key}
                        status = 200
                    else:
                        content = {"detail": ("Inactive user account.")}
                        status = 401
                else:
                    content = {"detail": ("Unverified user account.")}
                    status = 401
            else:
                content = {"detail": ("Invalid credentials, unable to signin.")}
                status = 401

        else:
            content = serializer.errors
            status = 400
        return Response(content, status)


class SignOutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[custom_user_schema.TOKEN_PARAMETER],
        responses=swagger_parameters.basic_response(
            200, {"Success": "User signed out"}, 400
        ),
    )
    def get(self, request, *args, **kwargs):
        tokens = SigninToken.objects.filter(user=request.user)
        for token in tokens:
            token.delete()
        content = {"Success": ("User signed out.")}
        status = 200

        return Response(content, status=status)


class RecoverPassword(GenericAPIView, UpdateModelMixin):
    """
    View to handle sending email with reset password link and
    changing password to a new one
    """

    http_method_names = ["post", "patch"]

    def get_queryset(self):
        if self.request.method == "POST":
            return User.objects.get_queryset_verified()
        elif self.request.method == "PATCH":
            code = self.request.query_params.get("code")
            return check_code_for_verification(code, PasswordResetCode).user

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            return ResetPasswordEmailSerializer(*args, **kwargs)
        else:
            return ResetPasswordSerializer(*args, **kwargs)

    def get_object(self):
        return self.get_queryset()

    @swagger_auto_schema(
        responses=swagger_parameters.basic_response(
            200,
            {"message": "Reset link was sucessfully send to given address email"},
            400,
        )
    )
    def post(self, request, *args, **kwargs):
        """
        Sends email with link to reset password for given email address
        """
        try:
            serializer = ResetPasswordEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.get_queryset().get(email=request.data.get("email"))
            reset_password_email(user)
        except User.DoesNotExist:
            raise CustomUserException("Account with given email does not exists")
        return Response(
            status=200, data="Reset link was sucessfully send to given address email"
        )

    @delete_used_token
    @swagger_auto_schema(
        manual_parameters=[custom_user_schema.signup_verify_parameters],
        responses=swagger_parameters.basic_response(
            200,
            {"message": "password changed successfully"},
            400,
        ),
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


@swagger_auto_schema(
    method="post",
    manual_parameters=[custom_user_schema.google_oauth_backend],
    request_body=SocialAuthSerializer,
    responses=swagger_parameters.basic_response(200, {"token": "token"}, 401),
)
@api_view(["POST"])
@psa()
def social_sign_google(request, backend):
    """View to exchange google API token for application authorization token
    If no user is associated with google token data, user will be created
    otherwise, user will be logged in
    """
    serializer = SocialAuthSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            user = request.backend.do_auth(request.data["access_token"])
        except AuthForbidden as e:
            raise CustomUserException(str(e))
        token, created = SigninToken.objects.get_or_create(user=user)

        return Response(status=200, data={"token": token.key})
