from rest_framework import serializers

from binder_environments import models


class BinderEnvironmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.BinderEnvironment
        fields = '__all__'
