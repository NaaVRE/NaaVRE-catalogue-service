from django.db import models

from base_assets.models import BaseAsset


class Workflow(BaseAsset):
    source_url = models.URLField(
        blank=True, verbose_name='source URL',
        help_text='URL workflows source file in naavrewf format',
        )
    run_url = models.URLField(
        blank=True, verbose_name='run URL',
        help_text='URL of the workflows execution (for example on argo)',
        )
    status = models.CharField(
        max_length=50, blank=True,
        help_text='Workflow status (example: Succeeded)',
        )
    progress = models.CharField(
        max_length=50, blank=True,
        help_text='Workflow progress (example: 5/5)'
        )
