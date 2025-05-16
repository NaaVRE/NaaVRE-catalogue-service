from rest_framework import serializers

from virtual_lab_instances import models


class VirtualLabInstanceSerializer(serializers.HyperlinkedModelSerializer):

    virtual_lab = serializers.ReadOnlyField(source='virtual_lab.slug')
    user = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        model = models.VirtualLabInstance
        fields = ['virtual_lab', 'user']
