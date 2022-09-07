from distutils.command.upload import upload
from django.contrib import admin
from django.urls import path
from .views import upload_photo

urlpatterns = [
    path('upload_photo/', upload_photo),
]