from django.contrib import admin

from base_assets.admin import (
    BaseAssetAdmin, BaseAssetAdminVersionMixin,
    BaseAssetVersionsCollectionAdmin,
    )
from . import models


@admin.register(models.BaseImage)
class BaseImageAdmin(admin.ModelAdmin):
    list_display = [
        "build",
        "runtime",
        ]


@admin.register(models.Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "module",
        "asname",
        ]


class BaseVariableAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        ]


@admin.register(models.Input)
class InputAdmin(BaseVariableAdmin):
    pass


@admin.register(models.Output)
class OutputAdmin(BaseVariableAdmin):
    pass


@admin.register(models.Conf)
class ConfAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "assignation",
        ]


@admin.register(models.Param)
class ParamAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "default_value",
        ]


@admin.register(models.Secret)
class SecretAdmin(BaseVariableAdmin):
    pass


@admin.register(models.Cell)
class CellAdmin(BaseAssetAdmin, BaseAssetAdminVersionMixin):
    versions_collection_model_class = models.CellVersionsCollection


@admin.register(models.CellVersionsCollection)
class CellVersionsCollectionAdmin(BaseAssetVersionsCollectionAdmin):
    versions_collection_model_class = models.CellVersionsCollection
