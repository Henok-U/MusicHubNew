from typing import List

from django.core.mail import send_mail

from MusicHub.config.settings import Common


def send_email(subject: str, message: str, to_email: List[str]) -> None | str:
    """
    Send email from musichub email address to subject or list of subjects
    return None if successful or error message
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=Common.EMAIL_FROM,
            recipient_list=to_email,
            fail_silently=False,
        )
    except Exception as e:
        return str(e)
