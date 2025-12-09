from file_assets.views import FileAssetViewSet

from . import models
from . import serializers


class NotebookFileViewSet(FileAssetViewSet):
    serializer_class = serializers.NotebookFileSerializer
    model_class = models.NotebookFile
