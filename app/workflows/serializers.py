from base_assets.serializers import BaseAssetSerializer

from . import models


class WorkflowSerializer(BaseAssetSerializer):

    class Meta(BaseAssetSerializer.Meta):
        model = models.Workflow
