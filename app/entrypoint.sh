#!/bin/bash

set -e

APP_PORT=${PORT:-8000}
cd /code/app/
python manage.py collectstatic --no-input
python manage.py wait_for_database
python manage.py migrate
python manage.py createsuperuser --no-input
gunicorn --worker-tmp-dir /dev/shm app.wsgi:application --bind "0.0.0.0:${APP_PORT}"
