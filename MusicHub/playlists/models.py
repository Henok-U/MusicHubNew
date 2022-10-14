from uuid import uuid4

from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models

from ..config.settings import Common
from ..main.utils import get_upload_path, get_sentinal_user


class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        unique=True,
        validators=[RegexValidator(regex="^[a-zA-Z0-9][a-zA-Z0-9\s\,\.\-]*$")],
    )
    is_public = models.BooleanField(default=True)
    playlist_image = models.ImageField(
        upload_to=get_upload_path,
        default="playlist/default/default.jpg",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )
    created_by = models.ForeignKey(
        Common.AUTH_USER_MODEL, on_delete=models.SET(get_sentinal_user)
    )
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name
