from django.db import models

from base_assets.models import BaseAsset


class FileAsset(BaseAsset):
    file = models.FileField(upload_to='files/', unique=True)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.file.name:
            self.file.storage.delete(self.file.name)
