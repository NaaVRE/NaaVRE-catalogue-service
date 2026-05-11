from django.contrib import admin

from . import models


@admin.register(models.NotebookFile)
class NotebookFileAdmin(admin.ModelAdmin):
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
