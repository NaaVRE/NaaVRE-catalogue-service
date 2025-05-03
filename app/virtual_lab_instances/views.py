from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication

from oidc_jwt_auth.authentication import OIDCAccessTokenBearerAuthentication
from . import models
from . import serializers


class VirtualLabInstanceViewSet(viewsets.ModelViewSet):
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
            return self.model.objects.filter(virtual_lab__slug=virtual_lab_slug)
        else:
            return self.model.objects.all()
