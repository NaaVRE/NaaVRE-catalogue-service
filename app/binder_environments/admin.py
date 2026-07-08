from django.contrib import admin

from . import models


@admin.register(models.BinderEnvironment)
class BinderEnvironmentAdmin(admin.ModelAdmin):
    list_display = [
        "binder_ref",
        "pre_pull",
        "container_image"
        ]
    list_filter = [
        "pre_pull",
        ]
