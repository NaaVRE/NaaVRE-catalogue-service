from base_assets.serializers import VersioningSerializerMixin
from file_assets.serializers import FileAssetSerializer

from . import models


class WorkflowFileSerializer(FileAssetSerializer, VersioningSerializerMixin):

    class Meta(FileAssetSerializer.Meta):
        model = models.WorkflowFile
        versions_collection_model = models.WorkflowFileVersionsCollection
