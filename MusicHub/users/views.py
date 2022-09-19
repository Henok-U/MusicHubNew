from authemail.models import PasswordResetCode, SignupCode
from authemail.views import SignupVerify
from django.contrib.auth import authenticate
from django.utils import timezone
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
    check_sigin_code,
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


class SignUpView(CreateAPIView):
    """
    View for signing up user
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
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
class SignUpVerifyView(SignupVerify):
    permission_classes = (permissions.AllowAny,)

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

    def get(self, request, *args, **kwargs):
        tokens = SigninToken.objects.filter(user=request.user)
        for token in tokens:
            checked_token = check_sigin_code(token, SigninToken)
            checked_token.delete()
        content = {"Succes": ("User signed out.")}
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

    @swagger_auto_schema(responses={200: "Message"})
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
        manual_parameters=[
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                description="String containing code from email link",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: "Message"},
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
    manual_parameters=[
        openapi.Parameter(
            "backend",
            openapi.IN_PATH,
            description="backend type - currently supporting only google-oauth2",
            type=openapi.TYPE_STRING,
        )
    ],
    request_body=SocialAuthSerializer,
    responses={200: "token - authorization token"},
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@psa()
def social_sign_google(request, backend):
    """View to exchange google API token for application authorization token
    If no user is associated with google token data, user will be created
    {backend} path should be set to 'google-oauth2'
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
