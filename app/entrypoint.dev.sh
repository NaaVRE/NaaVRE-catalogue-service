#!/bin/bash

set -e

cd /code/app/
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input || echo
python manage.py loaddata fixtures.json
python manage.py runserver 0.0.0.0:8000
