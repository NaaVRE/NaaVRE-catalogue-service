from rest_framework import serializers

from . import models


class VirtualLabLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualLabLabel
        fields = ['title', 'color']


class VirtualLabSerializer(serializers.HyperlinkedModelSerializer):
    labels = VirtualLabLabelSerializer(many=True, required=False)

    class Meta:
        model = models.VirtualLab
        fields = [
            'url',
            'slug',
            'title',
            'labels',
            'description',
            'created',
            'modified',
            'deployment_url',
            'container_image',
            'image',
            ]
