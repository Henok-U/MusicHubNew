from django.urls import path

from MusicHub.users.views.profile_view import AddUpdateProfilePicture

from .views import CreatePlaylistView, UpdatePlaylistView

urlpatterns = [
    path("create/", CreatePlaylistView.as_view(), name="create-playlist"),
    path("update/<str:pk>/", UpdatePlaylistView.as_view(), name="add-cover"),
]
