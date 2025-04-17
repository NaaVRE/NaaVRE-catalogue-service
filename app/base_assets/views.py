from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ParseError, ValidationError

from oidc_jwt_auth.authentication import OIDCAccessTokenBearerAuthentication
from virtual_labs.models import VirtualLab
from .permissions import IsOwner


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
    model_class: models.Model | None = None

    def get_queryset(self, *args, **kwargs):
        return self.model_class.objects.all().filter(owner=self.request.user)

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
