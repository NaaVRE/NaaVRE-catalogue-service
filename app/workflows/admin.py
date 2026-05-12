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
        "created",
        "modified",
        "run_url",
        "status",
        "progress",
        ]
    list_filter = [
        "owner",
        "virtual_lab",
        "shared_with_scopes",
        "status",
        ]
