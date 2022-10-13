from django.contrib import admin

from MusicHub.tracks.models import Track


class TrackAdmin(admin.ModelAdmin):
    def regroup_by(self):
        return "category"

    list_display = ("filename", "created_by", "track_length", "is_public", "playlist")
    list_filter = ("created_by", "is_public")
    readonly_fields = ("id", "created_at")
    ordering = ("created_by",)
    search_fields = ["filename", "created_by"]
    fields = (
        "filename",
        "id",
        "file",
        "track_length",
        "is_public",
        "created_at",
        "created_by",
        "playlist",
        "likes",
    )


admin.site.register(Track, TrackAdmin)
