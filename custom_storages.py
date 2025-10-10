from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


if getattr(settings, "STATICFILES_LOCATION", None):
    class StaticStorage(S3Boto3Storage):
        location = settings.STATICFILES_LOCATION
        default_acl = "public-read"
        file_overwrite = True


class MediaStorage(S3Boto3Storage):
    location = getattr(settings, "MEDIAFILES_LOCATION", "media")
    default_acl = "public-read"
    file_overwrite = False
