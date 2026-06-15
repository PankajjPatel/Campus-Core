#!/usr/bin/env bash
# exit on error
set -o errexit

python manage.py migrate
python manage.py seed_data
gunicorn CampusCore.wsgi:application --bind 0.0.0.0:$PORT
