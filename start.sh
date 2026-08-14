#!/usr/bin/env bash
python manage.py migrate --no-input || true
exec gunicorn CampusCore.wsgi:application --bind 0.0.0.0:${PORT:-10000}
