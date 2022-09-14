import os

from .settings import Common


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    INSTALLED_APPS += ("storages", )
    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"] 
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.getenv('DJANGO_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('DJANGO_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_AWS_STORAGE_BUCKET_NAME')
    

    DEFAULT_FILE_STORAGE = 'MusicHub.users.custom_storage.MediaStorage'
    AWS_STORAGE_BUCKET_NAME = "musichubstorage"
    AWS_DEFAULT_ACL = None
    MEDIA_URL = f'https://musichubstorage.s3.eu-central-1.amazonaws.com/'
    