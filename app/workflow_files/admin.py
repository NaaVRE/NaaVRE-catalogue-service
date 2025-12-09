from django.contrib import admin

from . import models


@admin.register(models.WorkflowFile)
class WorkflowFileAdmin(admin.ModelAdmin):
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
        "shared_with_scopes",
        ]
