from django.urls import path

from MusicHub.users.views.profile_view import AddUpdateProfilePicture

from .views import (
    CreatePlaylistView,
    UpdatePlaylistView,
    ListOwnPlaylistView,
    ListOwnPlaylistWithoutTrackPlaylist,
)

urlpatterns = [
    path("create/", CreatePlaylistView.as_view(), name="create-playlist"),
    path("update/<str:pk>/", UpdatePlaylistView.as_view(), name="add-cover"),
    path("list/", ListOwnPlaylistView.as_view(), name="list-own-playlist"),
    path(
        "list-for-add-track/",
        ListOwnPlaylistWithoutTrackPlaylist.as_view(),
        name="list-own-playlist-without-track",
    ),
]
