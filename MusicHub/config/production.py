import os

from .settings import Common


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
    INSTALLED_APPS += ("storages",)
    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]

    # Storage used for to integrade AWS S3 bucket with django
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    # AWS
    AWS_ACCESS_KEY_ID = os.getenv("DJANGO_AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("DJANGO_AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = "musichubstorage"
    AWS_DEFAULT_ACL = None

    # AWS S3 bucket
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_REGION_NAME = "eu-central-1"
    AWS_S3_VERIFY = True
    AWS_S3_FILE_OVERWRITE = False

    # Email links base url
    EMAIL_LINK_PATH = "http://3.71.253.142"
