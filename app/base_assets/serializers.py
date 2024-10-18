from rest_framework import serializers


class BaseAssetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    virtual_lab = serializers.ReadOnlyField(source='virtual_lab.slug')

    class Meta:
        fields = '__all__'
