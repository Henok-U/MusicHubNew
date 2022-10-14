from rest_framework.exceptions import ValidationError

MAX_PICTURE_SIZE = 3 * 1024 * 1024  # value in bytes, max 3Mb


def validate_picture(picture):
    if picture.size > MAX_PICTURE_SIZE:
        raise ValidationError("Picture size can not be greater than 3Mb")
