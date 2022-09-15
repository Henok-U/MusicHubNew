from distutils.command.upload import upload
from django.contrib import admin
from django.urls import path
from .views import CreateUserView, CreateUserVerify, RecoverPassword

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("create/verify/", CreateUserVerify.as_view(), name="create-verify"),
    path("reset-password/", RecoverPassword.as_view()),
]
