from base_assets.serializers import VersioningSerializerMixin
from file_assets.serializers import FileAssetSerializer

from . import models


class NotebookFileSerializer(FileAssetSerializer, VersioningSerializerMixin):

    class Meta(FileAssetSerializer.Meta):
        model = models.NotebookFile
        versions_collection_model = models.NotebookFileVersionsCollection
        fields = '__all__'
