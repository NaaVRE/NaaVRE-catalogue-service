import uuid

from django.db import models


class BinderEnvironment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    binder_ref = models.CharField(
        unique=True,
        max_length=500,
        help_text='Binder ref (e.g. gh/NaaVRE/vl-openlab/HEAD)',
        )
    container_image = models.CharField(
        blank=True,
        max_length=384,
        help_text='Container image of the binder environment',
        )
    pre_pull = models.BooleanField(default=False)

    def __str__(self):
        return self.binder_ref
