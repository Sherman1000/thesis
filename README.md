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

### 5. Configuración mínima en el admin

Para un uso normal de la aplicación, en el admin hay que dar de alta al menos:

1. **Un curso**  
   En *Cursos*: crear un curso (cuatrimestre y año). El sistema toma como “curso actual” el último curso creado. Sin al menos un curso, la importación de alumnos y otras funciones que dependen del curso actual pueden fallar.

Si vas a cargar alumnos por CSV desde el admin (*Importar estudiantes*), ese curso debe existir antes, porque los registros se asocian al curso actual.

### 6. Nota sobre CSRF si usás el admin

Si tenés sesión iniciada en el admin ([http://localhost/admin/](http://localhost/admin/)) y en la misma sesión del navegador entrás a la aplicación ([http://localhost](http://localhost)), algunas peticiones del frontend pueden fallar con **CSRF error**. Es por compartir cookies/sesión entre admin y app.

Para evitarlo: usar la app en otra pestaña en modo incógnito, en otro navegador, o cerrar sesión en el admin cuando estés probando la aplicación como alumno.

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
