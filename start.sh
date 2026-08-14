#!/usr/bin/env bash
set -o errexit
python manage.py migrate --no-input || true
python manage.py seed_data || true
gunicorn CampusCore.wsgi:application --bind 0.0.0.0:$PORT
