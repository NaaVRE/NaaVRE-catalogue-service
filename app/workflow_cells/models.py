from django.db import models

from base_assets.models import BaseAsset, VersioningMixin


class BaseImage(models.Model):
    build = models.CharField(
        max_length=384, blank=True,
        help_text=('Build stage base image (eg: '
                   'ghcr.io/qcdis/naavre/naavre-cell-build-python:v0.18)'),
        )
    runtime = models.CharField(
        max_length=384, blank=True,
        help_text=('Runtime stage base image (eg: '
                   'ghcr.io/qcdis/naavre/naavre-cell-runtime-python:v0.18)'),
        )

    def __str__(self):
        return f'{self.build}, {self.runtime}'


class Dependency(models.Model):
    name = models.CharField(max_length=255)
    module = models.CharField(blank=True, null=True, max_length=255)
    asname = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        verbose_name_plural = 'dependencies'

    def __str__(self):
        s = f'{self.name}'
        if self.module:
            s += f' from {self.module}'
        if self.asname:
            s += f' as {self.asname}'
        return s


class BaseVariable(models.Model):
    TYPE_CHOICES = {
        'int': 'Integer',
        'float': 'Float',
        'str': 'String',
        'list': 'List',
        }
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.name} ({self.type})'


class Input(BaseVariable):
    pass


class Output(BaseVariable):
    pass


class Conf(models.Model):
    name = models.CharField(max_length=255)
    assignation = models.TextField()

    def __str__(self):
        return f'{self.name} ({self.assignation})'


class Param(BaseVariable):
    default_value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.type}, {self.default_value})'


class Secret(BaseVariable):
    pass


class Cell(BaseAsset, VersioningMixin):
    container_image = models.CharField(
        max_length=384,
        help_text=('Containerized cell image (example: '
                   'ghcr.io/me/my-naavre-cells/my-cell-1:49c621b)'),
        )
    base_container_image = models.ForeignKey(
        BaseImage, blank=True, null=True,
        on_delete=models.PROTECT,
        )
    dependencies = models.ManyToManyField(Dependency, blank=True)
    inputs = models.ManyToManyField(Input, blank=True)
    outputs = models.ManyToManyField(Output, blank=True)
    confs = models.ManyToManyField(Conf, blank=True)
    params = models.ManyToManyField(Param, blank=True)
    secrets = models.ManyToManyField(Secret, blank=True)
    kernel = models.CharField(
        max_length=255, blank=True,
        help_text='Jupyter kernel of the source cell (example: ipython)',
        )
    source_url = models.URLField(
        blank=True,
        help_text=('URL of the folder on GitHub containing the sources of '
                   'the image (example: '
                   'https://github.com/me/my-NaaVRE-cells/tree'
                   '/2934de123c74316dc45fe84d340a7ca6914b8bc1/my-cell-1)'),
        )

    def __str__(self):
        return f'{super().__str__()} (v{self.version})'
