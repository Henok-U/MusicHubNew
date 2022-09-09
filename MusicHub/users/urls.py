from distutils.command.upload import upload
from django.contrib import admin
from django.urls import path
from .views import CreateUserView

urlpatterns = [
    path('create/', CreateUserView.as_view()),
]