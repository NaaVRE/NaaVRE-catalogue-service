from django.db import models

from base_assets.models import BaseAsset


class FileAsset(BaseAsset):
    file = models.FileField(upload_to='files/', unique=True)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.file.name:
            self.file.storage.delete(self.file.name)


class FileAssetCreationRequestQuerySet(models.QuerySet):
    def with_fileasset_created(self):
        return self.annotate(
            fileasset_created=models.Exists(
                FileAsset.objects.filter(file=models.OuterRef("file"))
            )
        )


class FileAssetCreationRequest(models.Model):
    """ FileAsset creation requests

    Tracks creation requests for FileAsset objects through the `presign`
    endpoint. This is used to ensure that no untracked objects are left in the
    S3 bucket.

    Lifecycle:
    - A new FileAssetCreationRequest is created when the presign endpoint is
      called. At this time, .file does not exist in the S3 bucket yet.
    - If the client uploads the file to S3 _and_ creates a corresponding
      FileAsset instance, the FileAsset's create handler removes the
      FileAssetCreationRequest instance.
    - If the client doesn't create a corresponding FileAsset instance, the
      FileAssetCreationRequest instance remains in the database.
    - Expired FileAssetCreationRequest instances can be cleaned up using the
      `cleanup_fileassetcreationrequests` management command. This will:
      - delete objects from S3 if they exist,
      - delete FileAssetCreationRequest instances.
    """
    file = models.FileField(upload_to='files/', unique=True)
    request_creation_date = models.DateTimeField(auto_now_add=True)

    objects = FileAssetCreationRequestQuerySet.as_manager()

    class Meta:
        ordering = ['request_creation_date']

    def __str__(self):
        return f'{self.file}'
