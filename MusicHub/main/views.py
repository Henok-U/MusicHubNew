from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from MusicHub.users.models import User
from MusicHub.users.custom_storage import MediaStorage
import os
@api_view(['GET'])
@parser_classes([JSONParser])
def is_server_working(request):
    variant = os.getenv('DJANGO_CONFIGURATION')
    try:
        User.objects.all()
        if variant == 'Production':
            media_storage = MediaStorage()
            media_storage.open('diagnostic/gandalf.jpg')
        return Response(status=200, data="Everything looks good!")
    except Exception as e:
            return Response(status=500, data=str(e))
