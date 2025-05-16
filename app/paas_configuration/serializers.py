from rest_framework import serializers

from . import models


class PaasConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaasConfiguration
        fields = ['title', 'description', 'documentation_url', 'site_icon']
