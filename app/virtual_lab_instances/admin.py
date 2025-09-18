from django.contrib import admin

from . import models


@admin.register(models.VirtualLabInstance)
class VirtualLabInstanceAdmin(admin.ModelAdmin):
    readonly_fields = ('date', )

    list_display = [
        "virtual_lab",
        "user",
        "date",
        ]
    list_filter = [
        "virtual_lab",
        "user",
        ]
