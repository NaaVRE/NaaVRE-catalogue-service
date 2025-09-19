from django.contrib import admin

from . import models


@admin.register(models.Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = [
        "source_url",
        "run_url",
        "status",
        "progress",
        ]
    list_display = [
        "__str__",
        "owner",
        "virtual_lab",
        # "version",
        # "next_version",
        "created",
        "modified",
        "run_url",
        "status",
        "progress",
        ]
    list_filter = [
        "owner",
        "virtual_lab",
        # "next_version",
        "shared_with_scopes",
        "status",
        ]
