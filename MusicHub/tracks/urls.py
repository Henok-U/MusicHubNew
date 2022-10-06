from django.urls import path

from .views import UploadTrackView

urlpatterns = [
    path("upload/", UploadTrackView.as_view(), name="upload-track"),
]
