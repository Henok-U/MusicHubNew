from django.core.mail import send_mail
from typing import List
from authemail.models import SignupCode


def send_email(subject: str, message: str, to_email: List[str]) -> None:
    send_mail(
        subject=subject,
        message=message,
        from_email="musichub.itechart@gmail.com",
        recipient_list=to_email,
        fail_silently=False,
    )


def trim_spaces_from_data(data):
    for key, value in data.items():
        data[key] = " ".join(value.split())
    return data


def verification_email(user, request):
    ipaddr = request.META.get("REMOTE_ADDR", "0.0.0.0")
    signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
    send_email(
        subject="Verify email account: ",
        message=f"http://localhost:8000/api/accounts/signup/verify/?code={signup_code}",
        to_email=[user.email],
    )
