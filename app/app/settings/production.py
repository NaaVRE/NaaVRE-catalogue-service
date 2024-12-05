import os

from app.settings.base import *  # noqa: F401 F403


def get_required_env(key):
    try:
        return os.environ[key]
    except KeyError:
        msg = f'Environment variable is required: {key}'
        raise EnvironmentError(msg)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_required_env('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = get_required_env('ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = get_required_env('CSRF_TRUSTED_ORIGINS').split(',')

CORS_ALLOWED_ORIGIN_REGEXES = get_required_env('CORS_ALLOWED_ORIGIN_REGEXES').split(',')
