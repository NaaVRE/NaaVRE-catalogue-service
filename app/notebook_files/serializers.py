from file_assets.serializers import FileAssetSerializer

from . import models


class NotebookFileSerializer(FileAssetSerializer):

    class Meta(FileAssetSerializer.Meta):
        model = models.NotebookFile
        fields = '__all__'
