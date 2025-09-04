from django.db import models
from django.core.validators import RegexValidator


class VirtualLabLabel(models.Model):
    title = models.CharField(
        unique=True,
        max_length=255,
        help_text="The display name of the label.",
        )
    color = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                message="Color must be a valid hex code, e.g., #FFF or #FFFFFF.",
                )
            ],
        help_text="Color in hex format (e.g. #FFFFFF).",
        )

    def __str__(self):
        return self.title


class VirtualLab(models.Model):
    slug = models.SlugField(primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    labels = models.ManyToManyField("VirtualLabLabel", related_name="VirtualLabs", blank=True)
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
