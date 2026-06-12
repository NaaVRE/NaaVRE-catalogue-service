from rest_framework import serializers
from django_pydantic_field.rest_framework import SchemaField

from . import models


class VirtualLabLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualLabLabel
        fields = ['title', 'color']


class VirtualLabSerializer(serializers.HyperlinkedModelSerializer):
    labels = VirtualLabLabelSerializer(many=True, required=False)
    additional_actions = SchemaField(list[models.AdditionalAction])

    class Meta:
        model = models.VirtualLab
        fields = [
            'url',
            'slug',
            'title',
            'labels',
            'description',
            'long_description',
            'created',
            'modified',
            'deployment_url',
            'additional_actions',
            'container_image',
            'binder_ref',
            'image',
            ]
