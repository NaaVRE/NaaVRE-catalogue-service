from django.db import models as django_models
from django.urls import reverse
from django.utils.html import format_html

from django.contrib import admin

from . import models


@admin.register(models.SharingScope)
class SharingScopeAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "title",
        "label"
        ]


class BaseAssetAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "owner",
        "virtual_lab",
        "version",
        "created",
        "modified",
        ]
    list_filter = [
        "owner",
        "virtual_lab",
        "shared_with_scopes",
        ]


class BaseAssetAdminVersionMixin(admin.ModelAdmin):
    versions_collection_model_class: django_models.Model

    readonly_fields = ["collection_link"]

    def _get_asset_versions_collection(self, obj) -> models.BaseAssetVersionsCollection:
        return getattr(
            obj,
            self.versions_collection_model_class._meta.model_name + '_set'
            ).first()

    @admin.display(description="Versions collection")
    def collection_link(self, obj):
        collection = self._get_asset_versions_collection(obj)
        if not collection:
            return "—"
        url = reverse((
                f"admin:"
                f"{self.versions_collection_model_class._meta.app_label}"
                f"_{self.versions_collection_model_class._meta.model_name}"
                f"_change"
            ),
            args=[collection.pk])
        return format_html('<a href="{url}">{collection}</a>', url=url, collection=collection)


class BaseAssetVersionsCollectionAdmin(admin.ModelAdmin):
    versions_collection_model_class: django_models.Model

    exclude = ["versions"]

    def get_inlines(self, request, obj):
        class AssetInline(admin.TabularInline):
            model = self.versions_collection_model_class.versions.through
            extra = 0

        return [AssetInline]
