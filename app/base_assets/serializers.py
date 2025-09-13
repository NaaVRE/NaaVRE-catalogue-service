from rest_framework import serializers

from . import models


class SharingScopeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SharingScope
        fields = '__all__'


class BaseAssetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    virtual_lab = serializers.ReadOnlyField(source='virtual_lab.slug')

    class Meta:
        fields = '__all__'
