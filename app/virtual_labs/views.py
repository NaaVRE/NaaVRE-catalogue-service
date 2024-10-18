from oidc_jwt_auth.authentication import OIDCAccessTokenBearerAuthentication
from rest_framework import permissions
from rest_framework import viewsets

from . import models
from . import serializers


class VirtualLabViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.VirtualLab.objects.all()
    serializer_class = serializers.VirtualLabSerializer
    authentication_classes = [OIDCAccessTokenBearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]
