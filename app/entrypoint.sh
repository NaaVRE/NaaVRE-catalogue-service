#!/bin/bash

set -e

APP_PORT=${PORT:-8000}
DEV_MODE=${DEV_MODE:-false}

cd "$(dirname "$0")"

python manage.py collectstatic --no-input
python manage.py wait_for_database
python manage.py wait_for_storage
$DEV_MODE && python manage.py makemigrations
python manage.py migrate
$DEV_MODE && python manage.py loaddata fixtures.json
python manage.py createsuperuser --no-input || echo
python manage.py create_serviceaccount naavre-environment-sa \
  -p binder_environments.binderenvironment.add_binderenvironment \
  -p binder_environments.binderenvironment.change_binderenvironment \
  -p binder_environments.binderenvironment.delete_binderenvironment \
  -p binder_environments.binderenvironment.view_binderenvironment \
  --token "${NAAVRE_ENVIRONMENT_SA_TOKEN}" || echo

if $DEV_MODE; then
  echo "Starting dev server"
  python manage.py runserver "0.0.0.0:${APP_PORT}"
else
  echo "Starting WSGI server"
  gunicorn --worker-tmp-dir /dev/shm app.wsgi:application --bind "0.0.0.0:${APP_PORT}"
fi
