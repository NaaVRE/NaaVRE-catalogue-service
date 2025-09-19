from django.contrib import admin

from . import models


@admin.register(models.OIDCUser)
class OIDCUserAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "uid",
        ]
