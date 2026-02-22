# Thesis – Programa de enseñanza (Django + React)

Proyecto que combina un **backend** en Django y un **frontend** en React, orquestados con Docker. En local se usa SQLite; en producción, PostgreSQL.

---

## Requisitos previos

- **Git**
- **Docker** y **Docker Compose** 
  - [Instalar Docker](https://docs.docker.com/get-docker/)
  - [Instalar Docker Compose](https://docs.docker.com/compose/install/)

---

## Desarrollo local: pasos para levantar el proyecto

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd thesis
```

### 2. Construir y levantar los contenedores

Desde la raíz del proyecto:

```bash
docker compose -f docker-compose-local.yml build
docker compose -f docker-compose-local.yml up
```

En local no hace falta ningún archivo `.env`: el backend usa SQLite (configurado en el compose local).

### 3. Crear un usuario administrador

Para acceder al panel de administración de Django:

```bash
./createsuperuser.sh
```

O manualmente:

```bash
docker compose -f docker-compose-local.yml exec backend sh -c "cd /app/backend && python manage.py createsuperuser"
```

### 4. Usar la aplicación

- **Aplicación (frontend):** [http://localhost](http://localhost)
- **Admin Django:** [http://localhost/admin/](http://localhost/admin/)

---

## Producción

### Configuración previa

1. Ajustar las URLs en `docker/nginx/production/default.conf` según el dominio/host que vayas a usar.
2. En el servidor, clonar el proyecto:
   ```bash
   git clone <url-del-repositorio>
   cd thesis
   ```
3. Copiar el ejemplo de variables de entorno y completar si es necesario:
   ```bash
   cp .env-example .env
   ```
   Editar `.env` con los valores de PostgreSQL que quieras usar (por defecto el ejemplo coincide con lo que espera el backend).
4. Certificados SSL (por ejemplo con Let's Encrypt):  
   [Tutorial recomendado](https://saasitive.com/tutorial/docker-compose-django-react-nginx-let-s-encrypt/)  
   En este proyecto suele usarse:
   ```bash
   ./init-letsencrypt.sh
   ```

### Levantar en producción

```bash
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up -d
```

(En producción se usa `docker-compose.yml`, no `docker-compose-local.yml`.)

### Actualizar después de cambios

```bash
git pull
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up -d
```

---

## Estructura del repositorio

| Elemento | Descripción |
|----------|-------------|
| **backend/** | Aplicación Django (API, modelos, admin). |
| **frontend/** | Aplicación React (interfaz del programa). |
| **docker/** | Dockerfiles y configuraciones de nginx (desarrollo y producción). |
| **docker-compose-local.yml** | Orquestación para desarrollo (backend + nginx, SQLite). |
| **docker-compose.yml** | Orquestación para producción (backend + nginx + PostgreSQL + certbot). |
| **createsuperuser.sh** | Script para crear un superusuario de Django con los contenedores levantados. |

En local, Docker construye el frontend (React) dentro de la imagen de nginx y sirve estáticos; el backend corre en otro contenedor y se accede por `/api`, `/admin` y `/media` a través de nginx.

Para más detalle del backend y del frontend, ver:

- [backend/README.md](backend/README.md)
- [frontend/README.md](frontend/README.md)
