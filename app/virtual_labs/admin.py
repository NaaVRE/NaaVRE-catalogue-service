from django.contrib import admin
from django.utils.html import format_html

from . import models


@admin.register(models.VirtualLabLabel)
class VirtualLabLabelAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "colored_color",
        ]

    @staticmethod
    def colored_color(obj):
        return format_html(
            '<span style="background:{};padding:4px;border-radius:100px;">{}</span>',
            obj.color,
            obj.color,
            )


@admin.register(models.VirtualLab)
class VirtualLabAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "title",
        "deployment_url",
        "container_image",
        "created",
        "modified",
        ]
