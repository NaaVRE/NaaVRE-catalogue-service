from django.db import models

from base_assets.models import BaseAssetVersionsCollection, VersioningMixin
from file_assets.models import FileAsset


class NotebookFile(FileAsset, VersioningMixin):
    pass


class NotebookFileVersionsCollection(BaseAssetVersionsCollection):
    versions = models.ManyToManyField(NotebookFile)
