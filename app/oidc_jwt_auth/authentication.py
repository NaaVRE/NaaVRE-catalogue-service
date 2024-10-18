import logging
import os
import ssl
from typing import Union

from django.contrib.auth.models import User
import jwt
import requests
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
    )
from rest_framework.exceptions import AuthenticationFailed

from .models import OIDCUser

logger = logging.getLogger()


class OIDCAccessTokenBearerAuthentication(BaseAuthentication):
    """ Authenticate with an OpenID Connect access token

    Clients should authenticate by passing an OIDC jwt access token in the
    "Authorization" HTTP header, prepended with the string "Bearer "

        Authorization: Bearer eyJhbGciOg...
    """

    keyword = 'Bearer'
    model = None

    def __init__(self):
        self.verify_ssl = self._get_verify_ssl()
        self.ssl_context = self._get_ssl_context(self.verify_ssl)
        self.openid_conf = self._get_openid_conf(self.verify_ssl)

    @staticmethod
    def _get_verify_ssl() -> bool:
        return os.getenv('VERIFY_SSL', 'true').lower() != 'false'

    @staticmethod
    def _get_ssl_context(verify_ssl: bool) -> ssl.SSLContext:
        if verify_ssl:
            return ssl.SSLContext()
        else:
            return ssl.SSLContext(verify_mode=ssl.CERT_NONE)

    @staticmethod
    def _get_openid_conf(verify_ssl: bool) -> Union[dict, None]:
        url = os.environ['OIDC_CONFIGURATION_URL']
        r = requests.get(url, verify=verify_ssl)
        r.raise_for_status()
        return r.json()

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = ('Invalid token header. Token string should not contain '
                   'spaces.')
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = ('Invalid token header. Token string should not contain '
                   'invalid characters.')
            raise AuthenticationFailed(msg)

        user = self.get_user(token)

        return user, token

    def validate_token(self, access_token):
        url = self.openid_conf['jwks_uri']
        jwks_client = jwt.PyJWKClient(url, ssl_context=self.ssl_context)

        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        token_header = jwt.get_unverified_header(access_token)
        try:
            data = jwt.decode(
                access_token,
                signing_key.key,
                algorithms=[token_header['alg']],
                audience="account",
                options={"verify_exp": True},
                )
        except jwt.exceptions.InvalidTokenError as e:
            logger.debug(msg="Authentication failed", exc_info=e)
            raise
        return data

    @staticmethod
    def validate_fake_token(access_token):
        """ Validate fake token for testing purpose

        This expects a jwt token using the HMAC+SHA (HS) algorithm and the
        secret 'fake-secret'
        """
        token_header = jwt.get_unverified_header(access_token)
        try:
            data = jwt.decode(
                access_token,
                'fake-secret',
                algorithms=[token_header['alg']],
                audience="account",
                options={"verify_exp": True},
                )
        except jwt.exceptions.InvalidTokenError as e:
            logger.debug(msg="Authentication failed", exc_info=e)
            raise
        return data

    def get_user(self, token):
        if os.getenv('DISABLE_AUTH', 'false').lower() == 'true':
            data = self.validate_fake_token(token)
        else:
            data = self.validate_token(token)
        uid = str(data['sub'])
        try:
            oidc_user = OIDCUser.objects.select_related('user').get(uid=uid)
            user = oidc_user.user
        except OIDCUser.DoesNotExist:
            if User.objects.filter(username=data.get('preferred_username')):
                msg = ('Cannot create User. A User with this username already '
                       'exists, but it is not linked to the token\'s OIDCUser')
                raise AuthenticationFailed(msg)
            user = User(username=data.get('preferred_username'))
            user.save()
            oidc_user = OIDCUser(uid=uid, user=user)
            oidc_user.save()
        return user

    def authenticate_header(self, request):
        return self.keyword
