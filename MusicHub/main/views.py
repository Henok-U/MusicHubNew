import os
from enum import auto

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from MusicHub.users.custom_storage import MediaStorage
from MusicHub.users.models import User

from .utils import send_email


@swagger_auto_schema(method="get", auto_schema=None)
@api_view(["GET"])
@parser_classes([JSONParser])
def is_server_working(request):
    variant = os.getenv("DJANGO_CONFIGURATION")
    try:
        User.objects.all()
        send_email(
            "Test message",
            "This is test message",
            ["Damian.Bednarek@itechart-group.com"],
        )
        if variant == "Production":
            media_storage = MediaStorage()
            media_storage.open("diagnostic/gandalf.jpg")
        return Response(status=200, data="Everything looks good!")
    except Exception as e:
        return Response(status=500, data=str(e))
