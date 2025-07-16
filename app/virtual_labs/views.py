from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import pagination

from . import models
from . import serializers


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
    filterset_fields = ['slug', 'title']
    search_fields = ['title', 'description']
    ordering_fields = ['slug', 'title', 'created', 'modified']
    pagination_class = VirtualLabPagination
