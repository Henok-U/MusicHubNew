from storages.backends.s3boto3 import S3Boto3Storage

from MusicHub.config import Production


class MediaStorage(S3Boto3Storage):
    bucket_name = "musichubstorage"
    