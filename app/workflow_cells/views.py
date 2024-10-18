from functools import reduce

from base_assets.views import BaseAssetViewSet
from . import models
from . import serializers


class CellViewSet(BaseAssetViewSet):
    serializer_class = serializers.CellSerializer
    model_class = models.Cell

    def destroy(self, request, *args, **kwargs):
        # List instances of nested fields
        instance = self.get_object()
        related_sets = [
            [instance.base_container_image],
            instance.dependencies.all(),
            instance.inputs.all(),
            instance.outputs.all(),
            instance.confs.all(),
            instance.params.all(),
            instance.secrets.all(),
            ]
        related_instances = reduce(
            lambda a, b: list(a) + list(b),
            related_sets
            )
        # destroy Cell instance
        resp = super().destroy(request, *args, **kwargs)
        # destroy orphan related instances
        for related_instance in related_instances:
            if not related_instance.cell_set.exists():
                related_instance.delete()
        return resp
