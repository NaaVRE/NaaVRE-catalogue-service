from django.db import models

from virtual_labs.models import VirtualLab


class VirtualLabInstance(models.Model):
    virtual_lab = models.ForeignKey(VirtualLab, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.username} on {self.virtual_lab.slug}'
