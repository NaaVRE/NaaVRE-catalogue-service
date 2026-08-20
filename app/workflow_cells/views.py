from functools import reduce

from django_filters.rest_framework import FilterSet, BooleanFilter
from django.db.models import Q

from base_assets.views import BaseAssetViewSet
from . import models
from . import serializers


class CellFilterSet(FilterSet):
    containerization_completed = BooleanFilter(
        method='filter_containerization_completed',
        label='Containerization completed',
        help_text=(
            'If true, only return cells whose containerization job status '
            'is "completed". If false, only return cells whose '
            'containerization job status is not "completed" (including '
            'cells without a containerization job). If unset, do not '
            'restrict the queryset.'
        ),
        )

    class Meta:
        model = models.Cell
        fields = BaseAssetViewSet.filterset_fields + ['containerization_completed']

    def filter_containerization_completed(self, queryset, name, value):
        completed_status = models.CellContainerizationJob.Status.COMPLETED
        filters = Q(containerization_job__isnull=False)
        if value:
            filters &= Q(containerization_job__status=completed_status)
        else:
            filters &= ~Q(containerization_job__status=completed_status)
        return queryset.filter(filters)


class CellViewSet(BaseAssetViewSet):
    serializer_class = serializers.CellSerializer
    model_class = models.Cell
    versions_collection_model_class = models.CellVersionsCollection
    filterset_class = CellFilterSet

    def destroy(self, request, *args, **kwargs):
        # List instances of nested fields
        instance = self.get_object()
        related_sets = [
            [instance.base_container_image, instance.containerization_job],
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
            if related_instance and not related_instance.cell_set.exists():
                related_instance.delete()
        return resp
