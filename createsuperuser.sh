#!/bin/sh
# Crear usuario admin de Django (entrar a http://localhost/admin/)
# Requiere que los contenedores estén levantados: docker-compose -f docker-compose-local.yml up

set -e
cd "$(dirname "$0")"

if command -v docker-compose >/dev/null 2>&1; then
  docker-compose -f docker-compose-local.yml exec backend sh -c "cd /app/backend && python manage.py createsuperuser"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  docker compose -f docker-compose-local.yml exec backend sh -c "cd /app/backend && python manage.py createsuperuser"
else
  echo "Necesitás Docker y docker-compose (o 'docker compose') instalados."
  exit 1
fi
