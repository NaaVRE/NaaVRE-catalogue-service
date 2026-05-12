from django.db import models as django_models
from django.db.models import OuterRef, Q, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ParseError, ValidationError

from oidc_jwt_auth.authentication import OIDCAccessTokenBearerAuthentication
from shared.pagination import ConfigurablePagination
from virtual_labs.models import VirtualLab
from .permissions import IsOwnerReadWriteOrSharedReadOnly
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
    pagination_class = ConfigurablePagination


class BaseAssetViewSet(viewsets.ModelViewSet):
    authentication_classes = [
        OIDCAccessTokenBearerAuthentication,
        SessionAuthentication,
        ]
    permission_classes = [permissions.IsAuthenticated, IsOwnerReadWriteOrSharedReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        ]
    filterset_fields = ['title', 'virtual_lab']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created', 'modified']

    # this should be overridden by children ViewSets
    model_class: django_models.Model
    versions_collection_model_class: django_models.Model | None = None

    @property
    def versions_collection_model_name(self) -> str:
        if not self.versions_collection_model_class:
            raise AttributeError(f'{self.__class__.__name__} has no versions_collection_model_class')
        elif self.versions_collection_model_class._meta.model_name is None:
            raise AttributeError(f'{self.versions_collection_model_class.__name__} has no name')
        else:
            return self.versions_collection_model_class._meta.model_name

    def get_queryset(self, *args, **kwargs):
        query_filters = Q()

        # owned by the user
        query_filters |= Q(owner=self.request.user)

        # shared with the user
        if self.action == 'list':
            shared_with_me = self.request.query_params.get('shared_with_me')
            if shared_with_me and shared_with_me.lower() == 'true':
                query_filters |= Q(shared_with_users=self.request.user)
        elif self.action == 'retrieve':
            query_filters |= Q(shared_with_users=self.request.user)

        # shared within scopes
        if self.action == 'list':
            shared_with_scopes = self.request.query_params.get('shared_with_scopes')
            if shared_with_scopes:
                for scope_slug in shared_with_scopes.split(','):
                    query_filters |= Q(shared_with_scopes__slug=scope_slug)
        elif self.action == 'retrieve':
            query_filters |= Q(shared_with_scopes__isnull=False)

        # latest version (last because it depends on the filters above)
        if self.action == 'list':
            all_versions = self.request.query_params.get('all_versions', 'true')
            if (self.versions_collection_model_class is not None) and (all_versions.lower() == 'false'):
                versions_collection_outer_ref = Q(**{
                    self.versions_collection_model_name: OuterRef(self.versions_collection_model_name),
                    })
                latest_in_collection = (
                    self.model_class.objects.filter(query_filters & versions_collection_outer_ref)
                    .order_by("-version")
                    .values("version")[:1]
                )
                query_filters &= Q(version=Subquery(latest_in_collection))

        queryset = (
            self.model_class.objects
                .filter(query_filters)
                .distinct()
            )

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
