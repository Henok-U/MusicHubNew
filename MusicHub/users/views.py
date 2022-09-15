from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import UserSerializer, CreateUserSerializer
from ..main.exception_handler import CustomUserException
from authemail.models import SignupCode
from authemail.views import SignupVerify
from MusicHub.main.utils import verification_email
from django.utils import timezone
from django.utils.decorators import method_decorator


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
        try:
            signup_code = SignupCode.objects.get(code=code)
        except SignupCode.DoesNotExist:
            raise CustomUserException("Verification code is not a valid code")
        now = timezone.now()
        diff = now - signup_code.created_at

        if diff.days * 24 > 24:
            raise CustomUserException("Token has expired.")
        verified = SignupCode.objects.set_user_is_verified(code)

        if verified:
            try:
                signup_code = SignupCode.objects.get(code=code)
                signup_code.delete()
            except SignupCode.DoesNotExist:
                pass
            content = {"success": ("Email address verified.")}
            return Response(data=content, status=200)
        else:
            content = {"detail": ("Unable to verify user.")}
            return Response(data=content, status=400)
