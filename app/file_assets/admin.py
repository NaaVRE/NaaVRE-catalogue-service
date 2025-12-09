from django.contrib import admin

from . import models


class InDBFilter(admin.SimpleListFilter):
    title = 'FileAsset created'
    parameter_name = 'fileasset_created'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Yes'),
            ('false', 'No'),
        )

    def queryset(self, request, qs):
        qs = qs.with_fileasset_created()
        value = self.value()
        if value == 'true':
            return qs.filter(fileasset_created=True)
        if value == 'false':
            return qs.filter(fileasset_created=False)
        return qs


@admin.register(models.FileAssetCreationRequest)
class FileAssetCreationRequestAdmin(admin.ModelAdmin):
    list_display = ('file', 'request_creation_date', 'fileasset_created')
    list_filter = (InDBFilter, )

    def fileasset_created(self, obj):
        return obj.fileasset_created

    fileasset_created.boolean = True
