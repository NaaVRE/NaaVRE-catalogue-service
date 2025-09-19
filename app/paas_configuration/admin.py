from django.contrib import admin

from . import models


@admin.register(models.PaasConfiguration)
class PaasConfigurationAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "documentation_url",
        # "site_icon__isnull",
        ]
