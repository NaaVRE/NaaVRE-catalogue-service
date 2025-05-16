from django.contrib import admin

from . import models


@admin.register(models.VirtualLabInstance)
class VirtualLabInstanceAdmin(admin.ModelAdmin):
    readonly_fields = ('date', )
