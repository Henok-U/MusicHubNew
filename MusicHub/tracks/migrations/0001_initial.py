# Generated by Django 4.1 on 2022-10-05 09:06

import MusicHub.tracks.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Track",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "filename",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="^[a-zA-Z0-9][a-zA-Z0-9\\s\\,\\.\\-]*$"
                            )
                        ],
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to=MusicHub.tracks.models.get_upload_path,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["mp3", "wav", "aac"]
                            )
                        ],
                    ),
                ),
                ("track_length", models.PositiveIntegerField(blank=True, null=True)),
                ("is_public", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
