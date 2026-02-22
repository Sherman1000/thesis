Iniciando
===============

## Descargar del repositorio utilizando --recurse-submodules

    $ git clone --recurse-submodule git@github.com:Sherman1000/thesis-desousa-wright.git

Recordar completar el archivo `.env`. Se deja un ejemplo en `.env-example`
    
## Instalar Docker & Docker Compose

https://docs.docker.com/compose/install/


## Build & up a los containers containers:

Antes que nada, `cd` al repo:

    $ cd /path/to/thesis
    $ sudo docker-compose -f docker-compose-local.yml build
    $ sudo docker-compose -f docker-compose-local.yml up

Para crear un usuario administrador y entrar al admin (http://localhost/admin/):

    $ ./createsuperuser.sh

O manualmente:

    $ docker-compose -f docker-compose-local.yml exec backend sh -c "cd /app/backend && python manage.py createsuperuser"

Deployment
==========

### Instalación en producción
Primero, se deberá ajustar el archivo `docker/nginx/production/default.conf` para utilizar las urls de la máquina deseada.

Luego, se debe ingresar a la máquina y descargar el proyecto. 

    $ git clone --recurse-submodule git@github.com:Sherman1000/thesis-desousa-wright.git

A continuación se deberá generar el certificado ssl (explicación aquí: https://saasitive.com/tutorial/docker-compose-django-react-nginx-let-s-encrypt/)

    $ cd thesis-desousa-wright    
    $ ./init-letsencrypt.sh

Luego de eso, ya estamos listos para levantar el sistema. Notar que estamos trabajando con `docker-compose.yml` y no con su contraparte local:

    $ sudo docker-compose -f docker-compose.yml build
    $ sudo docker-compose -f docker-compose.yml up -d

Listo! Tu aplicación está lista para utilizar. 

### Deploy de modificaciones al proyecto funcionando

    $ cd thesis-desousa-wright
    $ git pull --recurse-submodules
    $ sudo docker-compose -f docker-compose.yml build
    $ sudo docker-compose -f docker-compose.yml up -d


Explicación del Repo
==========

El repo consiste en dos submodules que manejan tanto backend como frontend. Este repo base se encarga de resolver docker y la inicialización del proyecto.

Se pueden encontrar los archivos para iniciar el proyecto con docker-compose tanto localmente como en producción.

En la carpeta `docker` se pueden encontrar los Dockerfile correspondientes al container de Backend y al de nginx (el cual sirve, además de nginx, al repo frontend).

A su vez, en la carpeta del container de nginx, además de su correspondiente Dockerfile, se pueden encontrar las configuraciones de nginx tanto para el ambiente local como para el de producción (que agrega certificados SSL para soportar https).