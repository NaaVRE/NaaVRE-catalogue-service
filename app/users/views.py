from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import pagination
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle

from oidc_jwt_auth.authentication import OIDCAccessTokenBearerAuthentication
from . import serializers


class SmallResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    max_page_size = 5


class UserViewSetRateThrottle(UserRateThrottle):
    rate = '600/hour'


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [
        OIDCAccessTokenBearerAuthentication,
        authentication.SessionAuthentication,
        ]
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallResultsSetPagination
    throttle_classes = [UserViewSetRateThrottle]

    def retrieve(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('GET')

    def get_queryset(self):
        if self.action == 'list':
            search = self.request.query_params.get("search")
            if not search or len(search) < 3:
                return User.objects.none()

            return User.objects.filter(
                Q(username__icontains=search)
                | Q(last_name__icontains=search)
            ).order_by("id")
        return []
