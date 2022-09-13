from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from .models import User
from .serializers import UserSerializer, CreateUserSerializer
from ..main.exception_handler import CustomUserException

from rest_framework.decorators import api_view, permission_classes
from social_django.utils import psa


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

        model_serializer = UserSerializer(data=serializer.data)
        model_serializer.is_valid(raise_exception=True)
        model_serializer.save()

        return Response(status=200, data=model_serializer.data)


# Create your views here.
@api_view(http_method_names=["POST"])
@permission_classes([permissions.AllowAny])
@psa()
def exchange_token(request, backend):
    # serializer = SocialSerializer(data=request.data)

    # if serializer.is_valid(raise_exception=True):
    # This is the key line of code: with the @psa() decorator above,
    # it engages the PSA machinery to perform whatever social authentication
    # steps are configured in your SOCIAL_AUTH_PIPELINE. At the end, it either
    # hands you a populated User model of whatever type you've configured in
    # your project, or None.
    user = request.backend.do_auth(request.data["access-token"])

    # if user:
    #     # if using some other token back-end than DRF's built-in TokenAuthentication,
    #     # you'll need to customize this to get an appropriate token object
    #     token, _ = Token.objects.get_or_create(user=user)
    #     return Response({'token': token.key})
    return Response(data=user)
    # else:
    #     return Response(
    #         {'errors': {'token': 'Invalid token'}},
    #         status=status.HTTP_400_BAD_REQUEST,
    #     )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_google_sign_link(request):
    return Response(
        data=f"https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fsocial%2Fgoogle-oauth2%2F&response_type=code&client_id=VlkYq8bqToZpMFW3omBJFUw6YVyzVxwvXBYndiyI&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile"
    )
