from rest_framework.serializers import ValidationError


def validate_files(data, max_size=None):
    if max_size and data.size > max_size:
        raise ValidationError("File cannot be bigger than %d Mb" % max_size)
