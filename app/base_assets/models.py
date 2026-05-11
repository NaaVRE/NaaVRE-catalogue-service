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
    show_in_virtual_labs = models.ManyToManyField(
        VirtualLab, related_name='visible_sharing_scopes', blank=True
        )
    check_in_virtual_labs = models.ManyToManyField(
        VirtualLab, related_name='checked_sharing_scopes', blank=True
        )

    def __str__(self):
        return f'{self.title} ({self.label})'


class VersioningMixin(models.Model):
    version = models.IntegerField(default=1)

    class Meta:
        abstract = True


class BaseAssetVersionsCollection(models.Model):
    """
    Subclasses FooVersionsCollection must define:
        versions = models.ManyToManyField(Foo)
    """
    class Meta:
        abstract = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls._meta.abstract:
            return
        has_versions = any(
            f.name == 'versions' and isinstance(f, models.ManyToManyField)
            for f in cls._meta.local_many_to_many
            )
        if not has_versions:
            raise TypeError(
                f"{cls.__name__} must define a ManyToManyField named 'versions'"
                )


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
