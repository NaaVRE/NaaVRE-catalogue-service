#!/bin/bash

set -e

APP_PORT=${PORT:-8000}
DEV_MODE=${DEV_MODE:false}

cd /code/app/

python manage.py collectstatic --no-input
python manage.py wait_for_database
python manage.py wait_for_storage
$DEV_MODE && python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input || echo
$DEV_MODE && python manage.py loaddata fixtures.json

if $DEV_MODE; then
  echo "Starting dev server"
  python manage.py runserver "0.0.0.0:${APP_PORT}"
else
  echo "Starting WSGI server"
  gunicorn --worker-tmp-dir /dev/shm app.wsgi:application --bind "0.0.0.0:${APP_PORT}"
fi
