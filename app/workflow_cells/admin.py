from django.contrib import admin

from . import models

admin.site.register(models.Cell)
admin.site.register(models.Input)
admin.site.register(models.Output)
admin.site.register(models.Conf)
admin.site.register(models.Param)
admin.site.register(models.Secret)
admin.site.register(models.BaseImage)
admin.site.register(models.Dependency)
