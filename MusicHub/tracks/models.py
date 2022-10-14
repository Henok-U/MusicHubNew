from uuid import uuid4

from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models

from ..main.utils import get_upload_path, get_sentinal_user
from ..config.settings import Common


class Track(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    filename = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        validators=[RegexValidator(regex="^[a-zA-Z0-9][a-zA-Z0-9\s\,\.\-]*$")],
    )

    file = models.FileField(
        upload_to=get_upload_path,
        blank=False,
        null=False,
        validators=[FileExtensionValidator(["mp3", "wav", "aac"])],
    )
    track_length = models.PositiveIntegerField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        Common.AUTH_USER_MODEL, on_delete=models.SET(get_sentinal_user)
    )
    playlist = models.ForeignKey(
        "playlists.Playlist",
        on_delete=models.CASCADE,
        to_field="name",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.filename
