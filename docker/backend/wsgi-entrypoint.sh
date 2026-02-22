#!/bin/sh

set -e
cd /app/backend

# Base vacía: migrate crea las tablas (SQLite o Postgres ya listo)
./manage.py migrate --noinput
./manage.py collectstatic --noinput

exec gunicorn backend.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

#####################################################################################
# Options to DEBUG Django server
# Optional commands to replace abouve gunicorn command

# Option 1:
# run gunicorn with debug log level
# gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 1 --threads 1 --log-level debug

# Option 2:
# run development server
# DEBUG=True ./manage.py runserver 0.0.0.0:8000