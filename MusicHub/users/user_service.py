from authemail.models import PasswordResetCode, SignupCode
from django.conf import settings
from django.utils import timezone

from MusicHub.users.models import User

from ..emailProvider.service import send_email
from ..main.exception_handler import CustomUserException


def verification_email(user, request):
    """Sent a verification email with link to the signed up user

    Args:
        user (User): Created user
        request (Request): Request

    Raises:
        CustomUserException: Error when sending email
    """
    ipaddr = request.META.get("REMOTE_ADDR", "0.0.0.0")
    signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
    error = send_email(
        subject="Verify email account: ",
        message=f"{settings.EMAIL_LINK_PATH}/api/user/signup/verify/?code={signup_code}",
        to_email=[user.email],
    )
    if error:
        raise CustomUserException(error)


def reset_password_email(user):
    """Sent a reset password email with link to the signed up user

    Args:
        user (User): User applying for password reset

    Raises:
        CustomUserException: Error when sending email
    """
    reset_code = PasswordResetCode.objects.create_password_reset_code(user)
    error = send_email(
        subject="Reset account password link: ",
        message=f"{settings.EMAIL_LINK_PATH}/api/user/reset-password/?code={reset_code}",
        to_email=[user.email],
    )
    if error:
        raise CustomUserException(error)


def has_token_expired(token):
    """Checks if token in links is not expired
    Returns:
        Boolean: True if token is expired, False otherwise
    """
    time = token.created_at + timezone.timedelta(days=1)
    if time < timezone.now():
        return True
    return False


def check_code_for_verification(code, objectModel):
    """
    Checks if verification code is valid ( not expired and not used)
    """
    try:
        verifiation_code = objectModel.objects.get(code=code)
    except objectModel.DoesNotExist:
        raise CustomUserException("Verification code is not a valid code")
    if has_token_expired(verifiation_code):
        raise CustomUserException("Token has expired.")

    return verifiation_code


def create_or_return_user(backend, response, *args, **kwargs):
    """Pipeline for social authentication
        responsible for creating new user or returning existing one

    Returns:
        User: created or pulled from database user
    """
    user, created = User.objects.get_or_create(
        email=response["sub"],
        first_name=response["given_name"],
        last_name=response["family_name"],
        password="",
        is_verified=True,
    )
    return user


def check_user_sign_up(func):
    def decorator(request, *args, **kwargs):
        user_query = User.objects.filter(email=request.data.get("email"))
        if user_query.exists():
            if user_query.get().is_verified:
                raise CustomUserException("Provided email address is already in use")

            if has_token_expired(SignupCode.objects.get(user=user_query.get())):
                signup_code = SignupCode.objects.get(user=user_query.get())
                signup_code.delete()
                verification_email(user_query.get(), request)
            raise CustomUserException("Please verify Your email address")
        response = func(request, *args, **kwargs)
        verification_email(user_query.get(), request)
        return response

    return decorator


def delete_used_token(func):
    def decorator(*args, **kwargs):
        reset_password = func(*args, **kwargs)
        view, request = args
        reset_code = PasswordResetCode.objects.get(
            code=request.query_params.get("code")
        )
        reset_code.delete()
        return reset_password

    return decorator
