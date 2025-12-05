from rest_framework import serializers

from base_assets.serializers import BaseAssetSerializer
from . import models
from .services.s3storage import S3StorageService


def key_exists_in_s3(key):
    if not S3StorageService().exists(key):
        raise serializers.ValidationError(
            'no object with this key exists in the bucket'
            )


def key_does_not_exist_in_db(key):
    qs = models.FileAsset.objects.filter(file=key)
    if qs.exists():
        raise serializers.ValidationError(
            'a record with this key already exists in the database'
            )


class FileAssetSerializer(BaseAssetSerializer):
    key = serializers.CharField(
        write_only=True,
        validators=[key_exists_in_s3, key_does_not_exist_in_db],
        )

    class Meta:
        model = models.FileAsset
        fields = ['id', 'file', 'key']
        read_only_fields = ['id', 'file']

    def create(self, validated_data):
        key = validated_data.pop('key')
        file = models.FileAsset(**validated_data)
        file.file.name = key
        file.save()
        return file


class PresignRequestSerializer(serializers.Serializer):
    filename = serializers.CharField()
    content_type = serializers.RegexField(r'^\w+/[-+.\w]+$')
