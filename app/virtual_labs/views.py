from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication

from oidc_jwt_auth.authentication import OIDCAccessTokenBearerAuthentication
from . import models
from . import serializers


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
