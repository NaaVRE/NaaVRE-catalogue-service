from django.contrib.auth.models import User
from django.db import models

from virtual_labs.models import VirtualLab


class VirtualLabInstance(models.Model):
    virtual_lab = models.ForeignKey(VirtualLab, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} on {self.virtual_lab}'
