from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
import os
from ..config.settings import Common

from uuid import uuid4


def get_upload_path(instance, filename):
    return os.path.join(
        "tracks",
        instance.created_by.get_email_short(),
        filename,
    )


class Track(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    filename = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        validators=[RegexValidator(regex="^[a-zA-Z0-9][a-zA-Z0-9\s\,\.\-]*$")],
    )
    track = models.FileField(
        upload_to=get_upload_path,
        blank=False,
        null=False,
        validators=[FileExtensionValidator(["mp3", "wav", "aac"])],
    )
    track_length = models.PositiveIntegerField(blank=True, null=True)
    public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Common.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.filename