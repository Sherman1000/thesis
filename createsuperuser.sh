#!/bin/sh
# Crear usuario admin de Django (entrar a http://localhost/admin/)
# Requiere que los contenedores estén levantados: docker compose -f docker-compose-local.yml up

set -e
cd "$(dirname "$0")"

if ! docker compose version >/dev/null 2>&1; then
  echo "Necesitás Docker con el plugin Compose (docker compose) instalado."
  exit 1
fi

docker compose -f docker-compose-local.yml exec backend sh -c "cd /app/backend && python manage.py createsuperuser"
