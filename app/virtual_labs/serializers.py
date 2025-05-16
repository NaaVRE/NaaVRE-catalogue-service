from rest_framework import serializers

from . import models


class VirtualLabSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.VirtualLab
        fields = ['url', 'slug', 'title', 'description', 'created', 'modified',
                  'deployment_url', 'container_image', 'image']
