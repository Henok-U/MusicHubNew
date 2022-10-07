from django.contrib import admin

from MusicHub.playlists.models import Playlist


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "is_public")
    fields = ("name", "is_public", "playlist_image", "created_by")


admin.site.register(Playlist, PlaylistAdmin)
