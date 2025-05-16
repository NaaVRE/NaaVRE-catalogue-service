from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError

from oidc_jwt_auth.authentication import OIDCAccessTokenBearerAuthentication
from virtual_labs.models import VirtualLab
from . import models
from . import serializers


class VirtualLabInstanceViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    serializer_class = serializers.VirtualLabInstanceSerializer
    authentication_classes = [
        OIDCAccessTokenBearerAuthentication,
        SessionAuthentication,
        ]
    permission_classes = [permissions.IsAuthenticated]

    model = models.VirtualLabInstance

    def get_queryset(self):
        virtual_lab_slug = self.request.query_params.get('virtual_lab', None)
        if virtual_lab_slug:
            queryset = self.model.objects.filter(virtual_lab__slug=virtual_lab_slug)
        else:
            queryset = self.model.objects.all()
        return queryset.distinct('user', 'virtual_lab')

    def _get_virtual_lab(self):
        try:
            slug = self.request.data['virtual_lab']
        except KeyError:
            raise ValidationError({'virtual_lab': ["This field is required."]})
        try:
            return VirtualLab.objects.get(slug=slug)
        except VirtualLab.DoesNotExist:
            raise ValidationError({'virtual_lab': ["The virtual lab does not exist."]})

    def perform_create(self, serializer):
        serializer.save(
            virtual_lab=self._get_virtual_lab(),
            user=self.request.user,
            )
