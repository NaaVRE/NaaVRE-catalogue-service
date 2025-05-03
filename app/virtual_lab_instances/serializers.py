from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from virtual_labs.models import VirtualLab
from . import models


class VirtualLabInstanceSerializer(serializers.HyperlinkedModelSerializer):

    virtual_lab = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=VirtualLab.objects.all()
        )

    class Meta:
        model = models.VirtualLabInstance
        fields = ['virtual_lab', 'username']

        validators = [
            UniqueTogetherValidator(
                queryset=models.VirtualLabInstance.objects.all(),
                fields=['virtual_lab', 'username'],
                )
            ]
