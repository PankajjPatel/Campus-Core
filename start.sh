#!/usr/bin/env bash
exec gunicorn CampusCore.wsgi:application --bind 0.0.0.0:${PORT:-10000}
