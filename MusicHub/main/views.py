from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from MusicHub.users.models import User
from MusicHub.users.custom_storage import MediaStorage

@api_view(['GET'])
def is_server_working(request):
    try:
        User.object.all()
        media_storage = MediaStorage()
        media_storage.open('https://musichubstorage.s3.eu-central-1.amazonaws.com/diagnostic/gandalf.jpg')
        return Response(status=200, data={
            "Database is working, \n AWS server and storage is working \n Everything looks good"})
    except FileNotFoundError:
        return Response(status=404, data={"Error while connecting to S3 storage"})
    except Exception as e:
            return Response(status=500, data={"Error while connecting to database"})
