from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from . import models
from . import serializers


class BinderEnvironmentViewSet(viewsets.ModelViewSet):
    queryset = models.BinderEnvironment.objects.all()
    serializer_class = serializers.BinderEnvironmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    model = models.BinderEnvironment

    filterset_fields = ['binder_ref', 'pre_pull']
    search_fields = ['binder_ref']
    ordering = ['binder_ref']
