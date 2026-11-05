from django_filters import BooleanFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from . import models
from . import serializers


class BinderEnvironmentFilter(FilterSet):
    has_container_image = BooleanFilter(method='filter_has_container_image')

    class Meta:
        model = models.BinderEnvironment
        fields = ['binder_ref', 'pre_pull']

    def filter_has_container_image(self, queryset, name, value):
        if value:
            return queryset.exclude(container_image='')
        return queryset.filter(container_image='')


class BinderEnvironmentViewSet(viewsets.ModelViewSet):
    queryset = models.BinderEnvironment.objects.all()
    serializer_class = serializers.BinderEnvironmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    model = models.BinderEnvironment

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        ]
    filterset_class = BinderEnvironmentFilter
    search_fields = ['binder_ref']
    ordering = ['binder_ref']
