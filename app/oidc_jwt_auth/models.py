from django.db import models
from django.contrib.auth.models import User


class OIDCUser(models.Model):
    uid = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "OIDC User"

    def __str__(self):
        return f'{self.user} ({self.uid})'
