from rest_framework.exceptions import ValidationError

from base_assets.views import BaseAssetViewSet

from . import models
from . import serializers


class CellViewSet(BaseAssetViewSet):
    serializer_class = serializers.CellSerializer
    model_class = models.Cell
