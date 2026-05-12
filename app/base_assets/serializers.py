from django.contrib.auth.models import User
from django.db import models as django_models
from django.urls import reverse
from rest_framework import serializers

from virtual_labs.models import VirtualLab
from . import models


class SharingScopeSerializer(serializers.HyperlinkedModelSerializer):
    show_in_virtual_labs = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field='slug',
        queryset=VirtualLab.objects.all(),
        )
    check_in_virtual_labs = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field='slug',
        queryset=VirtualLab.objects.all(),
        )

    class Meta:
        model = models.SharingScope
        fields = '__all__'


class VersioningSerializerMixin(serializers.HyperlinkedModelSerializer):
    versions = serializers.SerializerMethodField()

    class Meta:
        model: django_models.Model
        versions_collection_model: django_models.Model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not issubclass(self.Meta.model, models.VersioningMixin):
            raise Exception(
                f'{self.__class__.__name__} inherits VersioningSerializerMixin,'
                f' but {self.Meta.model.__name__} does not inherit from VersioningMixin')
        if not hasattr(self.Meta, 'versions_collection_model'):
            raise AttributeError(
                f'{self.__class__.__name__} inherits VersioningSerializerMixin,'
                f' but has no Meta.versions_collection_model'
                )

        self._model_detail_view_name = self.Meta.model._meta.model_name + '-detail'
        self.fields['previous_version'] = serializers.HyperlinkedRelatedField(
            required=False,
            write_only=True,
            queryset=self.Meta.model.objects.all(),
            view_name=self._model_detail_view_name
            )

    def _get_asset_versions_collection(self, obj) -> models.BaseAssetVersionsCollection:
        # get the VersionsCollection queryset related to AssetX previous_version
        # eg: if model_class is Cell, gets versions_collection.cellversionscollection_set
        assetversionscollection_set = getattr(
            obj,
            self.Meta.versions_collection_model._meta.model_name + '_set'
            )
        # get the asset_versions_collection
        if (count := assetversionscollection_set.count()) != 1:
            raise ValueError(
                f"{self.Meta.model.__name__} '{obj}'"
                f" has {count} {self.Meta.versions_collection_model.__name__}"
                )
        return assetversionscollection_set.first()

    def create(self, validated_data):
        previous_asset = validated_data.pop('previous_version', None)
        if previous_asset is None:
            # create a new assets_versions_collection for the
            versions_collection = self.Meta.versions_collection_model.objects.create()
            validated_data['version'] = 1
        else:
            versions_collection = self._get_asset_versions_collection(previous_asset)
            last_version = versions_collection.versions.aggregate(django_models.Max('version'))['version__max']
            validated_data['version'] = last_version + 1
        asset = super().create(validated_data)
        versions_collection.versions.add(asset)
        return asset

    def get_versions(self, obj):
        request = self.context["request"]
        versions_collection = self._get_asset_versions_collection(obj)
        if versions_collection is None:
            return []
        return [
            {
                "version": asset.version,
                "url": request.build_absolute_uri(
                    reverse(self._model_detail_view_name, args=[asset.pk])
                    )
                }
            for asset in versions_collection.versions.order_by('version')
        ]


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
