from django.db import models as django_models
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ParseError, ValidationError

from oidc_jwt_auth.authentication import OIDCAccessTokenBearerAuthentication
from virtual_labs.models import VirtualLab
from .permissions import IsOwner
from . import serializers
from . import models


class SharingScopeViewset(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [
        OIDCAccessTokenBearerAuthentication,
        SessionAuthentication,
        ]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SharingScopeSerializer
    queryset = models.SharingScope.objects.all()
    model_class = models.SharingScope


class BaseAssetViewSet(viewsets.ModelViewSet):
    authentication_classes = [
        OIDCAccessTokenBearerAuthentication,
        SessionAuthentication,
        ]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        ]
    filterset_fields = ['title', 'virtual_lab']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created', 'modified']

    # this should be overridden by children ViewSets
    model_class: django_models.Model | None = None

    def get_queryset(self, *args, **kwargs):
        # 1. Include filters
        q_include = Q()

        # owned by the user
        q_include |= Q(owner=self.request.user)

        # 2. Exclusion filters
        q_exclude = Q()

        # non-current versions
        if hasattr(self.model_class, 'next_version'):
            if self.action == 'list':
                all_versions = self.request.query_params.get('all_versions')
                if not (all_versions and all_versions.lower() == 'true'):
                    q_exclude |= Q(next_version__isnull=False)

        queryset = self.model_class.objects.filter(q_include).exclude(q_exclude)

        return queryset

    def _get_virtual_lab(self):
        try:
            slug = self.request.data['virtual_lab']
        except KeyError:
            raise ValidationError({'virtual_lab': ["This field is required."]})
        try:
            return VirtualLab.objects.get(slug=slug)
        except VirtualLab.DoesNotExist:
            raise ParseError('virtual lab does not exist')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        serializer.save(virtual_lab=self._get_virtual_lab())
