from botocore.exceptions import EndpointConnectionError
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import default_storage
from storages.backends.s3 import S3Storage


class S3StorageService:
    storage: S3Storage

    def __init__(self):
        if not isinstance(default_storage, S3Storage):
            raise ImproperlyConfigured(
                f'unsupported storage: {default_storage.__class__.__name__}. '
                'Use storages.backends.s3.S3Storage as the default storage to '
                'enable presigned upload.'
                )
        self.storage = default_storage

    def generate_presigned_upload_url(
            self, filename, content_type, expire=None
            ):
        key = self.storage.get_available_name(filename)

        if expire is None:
            expire = self.storage.querystring_expire

        url = self.storage.connection.meta.client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.storage.bucket.name,
                "Key": key,
                "ContentType": content_type,
                },
            ExpiresIn=expire,
            HttpMethod='PUT',
            )
        return key, url

    def exists(self, key):
        return self.storage.exists(key)

    def check_connection(self):
        self.storage.connection.meta.client.head_bucket(Bucket=self.storage.bucket.name)
