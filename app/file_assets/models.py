from django.db import models

from base_assets.models import BaseAsset


class FileAsset(BaseAsset):
    file = models.FileField(upload_to='files/', unique=True)
