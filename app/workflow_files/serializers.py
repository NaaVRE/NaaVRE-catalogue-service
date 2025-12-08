from file_assets.serializers import FileAssetSerializer

from . import models


class WorkflowFileSerializer(FileAssetSerializer):

    class Meta(FileAssetSerializer.Meta):
        model = models.WorkflowFile
