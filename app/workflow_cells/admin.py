from django.contrib import admin

from . import models


@admin.register(models.BaseImage)
class BaseImageAdmin(admin.ModelAdmin):
    list_display = [
        "build",
        "runtime",
        ]


@admin.register(models.Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "module",
        "asname",
        ]


class BaseVariableAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        ]


@admin.register(models.Input)
class InputAdmin(BaseVariableAdmin):
    pass


@admin.register(models.Output)
class OutputAdmin(BaseVariableAdmin):
    pass


@admin.register(models.Conf)
class ConfAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "assignation",
        ]


@admin.register(models.Param)
class ParamAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "default_value",
        ]


@admin.register(models.Secret)
class SecretAdmin(BaseVariableAdmin):
    pass


@admin.register(models.Cell)
class CellAdmin(admin.ModelAdmin):
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
