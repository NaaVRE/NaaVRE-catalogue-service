from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, BaseInFilter
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import pagination

from . import models
from . import serializers


class VirtualLabFilter(FilterSet):
    labels = BaseInFilter(
        field_name="labels__title",
        lookup_expr="in",
        distinct=True,
    )

    class Meta:
        model = models.VirtualLab
        fields = {
            'slug': ['exact'],
            'title': ['exact'],
            'is_pinned': ['exact'],
        }


class VirtualLabPagination(pagination.PageNumberPagination):
    page_size = 1000


class VirtualLabViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.VirtualLab.objects.all()
    serializer_class = serializers.VirtualLabSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        ]
    filterset_class = VirtualLabFilter
    search_fields = ['title', 'description']
    ordering_fields = ['slug', 'title', 'created', 'modified', 'pinned_order']
    ordering = ['title']
    pagination_class = VirtualLabPagination


class VirtualLabLabelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.VirtualLabLabel.objects.all()
    serializer_class = serializers.VirtualLabLabelSerializer
