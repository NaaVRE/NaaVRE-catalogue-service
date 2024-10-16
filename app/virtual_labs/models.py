import uuid

from django.db import models


class VirtualLab(models.Model):
    slug = models.SlugField(primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deployment_url = models.URLField(
        blank=True, verbose_name='URL',
        help_text='URL of the virtual lab deployment',
        )
    container_image = models.CharField(
        max_length=100, blank=True,
        help_text='Container image of the virtual lab',
        )

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.slug
