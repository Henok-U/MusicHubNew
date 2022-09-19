from authemail.models import PasswordResetCode, SignupCode
from authemail.views import SignupVerify
from django.contrib.auth import authenticate
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.authtoken.models import Token as SigninToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from social_core.exceptions import AuthForbidden
from social_django.utils import psa

from MusicHub.main.utils import (
    check_code_for_verification,
    has_token_expired,
    reset_password_email,
    verification_email,
)

from ..main.exception_handler import CustomUserException
from .models import User
from .serializers import (
    ResetPasswordEmailSerializer,
    ResetPasswordSerializer,
    SigninSerializer,
    SignupSerializer,
    SocialAuthSerializer,
)
from . import custom_user_schema


class SignUpView(GenericAPIView):
    """
    View for signing up user
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = SignupSerializer

    @swagger_auto_schema(responses=custom_user_schema.signup_return_schema)
    def post(self, request, *args, **kwargs):
        queryset = User.objects.filter(email=request.data["email"])

        if queryset.exists():
            if queryset.get().is_verified:
                raise CustomUserException("Provided email address is already in use")

            if has_token_expired(SignupCode.objects.get(user=queryset.get()), 24):
                signup_code = SignupCode.objects.get(user=queryset.get())
                signup_code.delete()
                verification_email(queryset.get(), request)
            raise CustomUserException("Please verify Your email address")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        verification_email(user, request)

        return Response(status=200, data=serializer.data)


class SignUpVerifyView(SignupVerify):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        manual_parameters=custom_user_schema.signup_verify_parameters,
        responses=custom_user_schema.signup_verify_response,
    )
    def get(self, request, format=None):

        try:
            code = request.query_params["code"]
            verification_code = check_code_for_verification(code, SignupCode)
            verification_code.user.is_verified = True
            verification_code.user.save()
            verification_code.delete()
        except MultiValueDictKeyError:
            raise CustomUserException("Please provide code parameter")
        return Response(data="Email address verified.", status=200)


class SignInView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SigninSerializer

    @swagger_auto_schema(
        request_body=custom_user_schema.signin_request_schema,
        responses=custom_user_schema.signin_return_schema,
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
        manual_parameters=custom_user_schema.signout_parameters,
        responses=custom_user_schema.signout_verify_response,
    )
    def get(self, request, *args, **kwargs):
        tokens = SigninToken.objects.filter(user=request.user)
        for token in tokens:
            token.delete()
        content = {"Success": ("User signed out.")}
        status = 200

        return Response(content, status=status)


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

    @swagger_auto_schema(responses=custom_user_schema.reset_password_returns)
    def post(self, request, format=None):
        """
        Sends email with link to reset password for given email address
        """
        try:
            serializer = ResetPasswordEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.queryset.get(email=request.data["email"])
            reset_password_email(user)
        except User.DoesNotExist:
            raise CustomUserException("Account with given email does not exists")
        return Response(
            status=200, data="Reset link was sucessfully send to given address email"
        )

    @swagger_auto_schema(
        manual_parameters=[custom_user_schema.reset_password_query],
        responses=custom_user_schema.reset_password_returns,
    )
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

        user = reset_code.user
        user.set_password(request.data["password"])
        user.save()
        reset_code.delete()

        return Response(status=200, data="Password was successfully changed")


@swagger_auto_schema(
    method="post",
    manual_parameters=[custom_user_schema.google_oauth_backend],
    request_body=SocialAuthSerializer,
    responses=custom_user_schema.google_oauth_return,
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@psa()
def social_sign_google(request, backend):
    """View to exchange google API token for application authorization token
    If no user is associated with google token data, user will be created
    otherwise, user will be logged in
    """

    if not backend == "google-oauth2":
        raise CustomUserException("Given backend provider is not valid")

    serializer = SocialAuthSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            user = request.backend.do_auth(request.data["access_token"])
        except AuthForbidden as e:
            raise CustomUserException(str(e))
        token, created = SigninToken.objects.get_or_create(user=user)

        return Response(status=200, data={"token": token.key})

    return Response(status=400, data="Error during signing")
