from django.contrib import admin

from . import models

admin.site.register(models.VirtualLabLabel)
admin.site.register(models.VirtualLab)
