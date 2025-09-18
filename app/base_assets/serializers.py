from django.contrib.auth.models import User
from rest_framework import serializers

from . import models


class SharingScopeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SharingScope
        fields = '__all__'


class BaseAssetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    virtual_lab = serializers.ReadOnlyField(source='virtual_lab.slug')
    shared_with_scopes = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=models.SharingScope.objects.all(),
        )
    shared_with_users = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field='username',
        queryset=User.objects.all(),
        )

    class Meta:
        fields = '__all__'
