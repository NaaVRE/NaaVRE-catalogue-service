import os

from app.settings.base import *  # noqa: F401 F403


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f97*o+o+%z$e@d&3=n6%+)jt$^r10%yk9)ul2a8zlfy1$-n41^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', [])
if ALLOWED_HOSTS:
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', [])
if CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS.split(',')

CORS_ALLOWED_ORIGIN_REGEXES = os.getenv('CORS_ALLOWED_ORIGIN_REGEXES', [])
if CORS_ALLOWED_ORIGIN_REGEXES:
    CORS_ALLOWED_ORIGIN_REGEXES = CORS_ALLOWED_ORIGIN_REGEXES.split(',')
