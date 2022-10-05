from django.contrib import admin

from MusicHub.tracks.models import Track


class TrackAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "created_at", "created_by")
    fields = (
        "filename",
        "id",
        "file",
        "track_length",
        "is_public",
        "created_at",
        "created_by",
    )


admin.site.register(Track, TrackAdmin)
