from file_assets.views import FileAssetViewSet

from . import models
from . import serializers


class WorkflowFileViewSet(FileAssetViewSet):
    serializer_class = serializers.WorkflowFileSerializer
    model_class = models.WorkflowFile
