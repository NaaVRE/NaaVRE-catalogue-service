import uuid

from django.contrib.auth.models import User
from django.db import models

from virtual_labs.models import VirtualLab


class SharingScope(models.Model):
    slug = models.SlugField(primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    LABEL_CHOICES = {
        'virtual_lab': 'Virtual Lab',
        'community': 'Community',
        }
    label = models.CharField(max_length=100, choices=LABEL_CHOICES)

    def __str__(self):
        return f'{self.title} ({self.label})'


class VersioningMixin(models.Model):
    version = models.IntegerField(default=1)
    next_version = models.ForeignKey(
        "self", on_delete=models.SET_NULL,
        null=True, blank=True,
        )

    class Meta:
        abstract = True


class BaseAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name='assets', on_delete=models.CASCADE,
        )
    virtual_lab = models.ForeignKey(
        VirtualLab, related_name='assets', null=True,
        on_delete=models.SET_NULL,
        )
    shared_with_scopes = models.ManyToManyField(SharingScope, blank=True)
    shared_with_users = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'{self.title}-{self.owner.username}'
