from django.contrib import admin

from base_assets.admin import (
    BaseAssetAdmin, BaseAssetAdminVersionMixin,
    BaseAssetVersionsCollectionAdmin,
    )
from . import models


@admin.register(models.WorkflowFile)
class WorkflowFileAdmin(BaseAssetAdmin, BaseAssetAdminVersionMixin):
    versions_collection_model_class = models.WorkflowFileVersionsCollection


@admin.register(models.WorkflowFileVersionsCollection)
class CellVersionsCollectionAdmin(BaseAssetVersionsCollectionAdmin):
    versions_collection_model_class = models.WorkflowFileVersionsCollection
