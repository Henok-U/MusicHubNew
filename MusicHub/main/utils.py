from django.core.mail import send_mail
from typing import List


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
