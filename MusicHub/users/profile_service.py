from rest_framework.serializers import ValidationError


def validate_passwords_match(data):
    """
    validate password and confrim password field to be the same
    """

    if not data.get("password") == data.get("confirm_password"):
        raise ValidationError("Passwords does not match")


def validate_old_password(data, user):
    """
    Validate if the old password is valid and new password is different from old password
    """

    if not user.check_password(data.get("old_password")):
        raise ValidationError("Invalid old password")
    if data.get("password") == data.get("old_password"):
        raise ValidationError("Old password and new password cannot be the same")
