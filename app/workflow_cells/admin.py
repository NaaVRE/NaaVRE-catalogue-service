from django.contrib import admin

from . import models


class CellAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "owner",
        "virtual_lab",
        "version",
        "next_version",
        "created",
        "modified",
        ]
    list_filter = [
        "owner",
        "virtual_lab",
        "next_version",
        ]


admin.site.register(models.Cell, CellAdmin)
admin.site.register(models.Input)
admin.site.register(models.Output)
admin.site.register(models.Conf)
admin.site.register(models.Param)
admin.site.register(models.Secret)
admin.site.register(models.BaseImage)
admin.site.register(models.Dependency)
