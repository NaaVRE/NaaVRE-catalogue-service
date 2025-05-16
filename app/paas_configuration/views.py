from rest_framework import viewsets

from . import models
from . import serializers


class PaasConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.PaasConfiguration.objects.all()
    serializer_class = serializers.PaasConfigurationSerializer
