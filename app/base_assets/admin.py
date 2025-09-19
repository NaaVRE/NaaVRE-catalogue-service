from django.contrib import admin

from . import models


@admin.register(models.SharingScope)
class SharingScopeAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "title",
        "label"
        ]
