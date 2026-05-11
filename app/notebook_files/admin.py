from django.contrib import admin

from base_assets.admin import (
    BaseAssetAdmin, BaseAssetAdminVersionMixin,
    BaseAssetVersionsCollectionAdmin,
    )
from . import models


@admin.register(models.NotebookFile)
class NotebookFileAdmin(BaseAssetAdmin, BaseAssetAdminVersionMixin):
    versions_collection_model_class = models.NotebookFileVersionsCollection


@admin.register(models.NotebookFileVersionsCollection)
class CellVersionsCollectionAdmin(BaseAssetVersionsCollectionAdmin):
    versions_collection_model_class = models.NotebookFileVersionsCollection
