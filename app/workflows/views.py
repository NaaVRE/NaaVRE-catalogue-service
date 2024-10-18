from base_assets.views import BaseAssetViewSet

from . import models
from . import serializers


class WorkflowViewSet(BaseAssetViewSet):
    serializer_class = serializers.WorkflowSerializer
    model_class = models.Workflow
