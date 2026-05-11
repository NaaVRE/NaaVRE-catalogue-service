from django.db import models

from base_assets.models import BaseAssetVersionsCollection, VersioningMixin
from file_assets.models import FileAsset


class WorkflowFile(FileAsset, VersioningMixin):
    pass


class WorkflowFileVersionsCollection(BaseAssetVersionsCollection):
    versions = models.ManyToManyField(WorkflowFile)
