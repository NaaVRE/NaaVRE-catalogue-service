from django.db import models
from django.core.validators import RegexValidator

from django_pydantic_field import SchemaField
from pydantic import BaseModel, Field


color_regex = r'^#(?:[0-9a-fA-F]{3}){1,2}$'


# We represent AdditionalActions as a pydantic model that gets serialized in a
# JSONField at VirtualLab.additional_actions.
# This allows for two things:
# - avoiding a separate table for this data that is strictly subordinate of a
#   given VirtualLab
# - having an ordered list without extra steps (getting this with a m2m field
#   requires extra code)
# The tradeoff is that no automatic database migrations are created if the
# pydantic schema is updated, because it is not managed by Django.
# If the schema is updated, existing values of VirtualLab.additional_action
# will stay on the old schema, unless a manual migration is created.
# Hence, the following WARNING:
# WARNING: DO NOT MODIFY THIS MODEL'S SCHEMA UNLESS YOU ALSO ADD A MANUAL
# MIGRATION FOR EXISTING VirtualLab.additional_action FIELDS IN THE DB.
class AdditionalAction(BaseModel):
    label: str = Field(max_length=255)
    url: str = Field(max_length=1000)
    color: str = Field(default=None, pattern=color_regex)


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
                regex=color_regex,
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
    description = models.TextField(
        blank=True,
        help_text="Short description of the virtual lab",
        )
    long_description = models.TextField(
        blank=True,
        help_text="Markdown-formatted description of the virtual lab",
        )
    is_pinned = models.BooleanField(default=False)
    pinned_order = models.IntegerField(default=-1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deployment_url = models.URLField(
        max_length=1000, blank=True, verbose_name='URL',
        help_text='URL of the virtual lab deployment',
        )
    additional_actions: list[AdditionalAction] = SchemaField(default=list, blank=True)
    container_image = models.CharField(
        max_length=384, blank=True,
        help_text='Container image of the virtual lab',
        )
    binder_ref = models.CharField(
        max_length=500, blank=True,
        help_text='Binder ref (e.g. gh/NaaVRE/vl-openlab/HEAD)',
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
