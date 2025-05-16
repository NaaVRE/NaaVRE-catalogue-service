from django.db import models


class VirtualLab(models.Model):
    slug = models.SlugField(primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deployment_url = models.URLField(
        blank=True, verbose_name='URL',
        help_text='URL of the virtual lab deployment',
        )
    container_image = models.CharField(
        max_length=384, blank=True,
        help_text='Container image of the virtual lab',
        )
    image = models.TextField(
        null=True,
        blank=True,
        help_text=("Base 64-encoded image with a resolution of minimum "
                   "100x100 px. E.g. \"data:image/png;base64,[...]\""),
        )

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.slug
