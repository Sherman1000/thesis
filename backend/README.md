Backend
===============
 
App Folder
==========
Carpeta que tiene la mayor parte de la aplicación funcional.

El modelo está dividido en `commands`, `endpoints`, `entities` y `presenters`. A su vez, se mantienen los modelos de Django para la persistencia en la carpeta `models` y sus respectivas migraciones en `migrations`.

### Commands
### Endpoints
### Entities
### Presenters

Backend Folder
==========

Archivos necesarios para el funcionamiento de Django. Prestar especial atención a `settings.py` y `urls.py`, donde aparecen variables de configuración del sistema (algunas pueden ser necesarias de modificar para entornos de producción distintos) y las urls de los endpoints del sistema.


Templates Folder
==========

Django templates utilizados desde el admin para importar csv y modificar los listados de los modelos de Django. Separados por modelo al que están asociados. 



Como realizar un Backup de la base de producción 
==========

    $ cd /path/to/thesis
    $ sudo docker exec thesis-desousa-wright_db_1 pg_dump -U hello_django hello_django_dev > backup_latest

Luego localmente correr:

    $ scp site@10.10.0.215:thesis-desousa-wright/backup_latest .

Para restaurar el Backup se debe hacer: 

    $ sudo psql -U postgres tesis < backup_latest

donde tesis es el nombre de una base nueva creada con 

    $ sudo -u postgres createdb tesis

donde postgres es un usuario de postgres (importante acordarse la contraseña!)


Dejo link por si no te acordas:
https://stackoverflow.com/questions/14588212/postgresql-resetting-password-of-postgresql-on-ubuntu


Como realizar un Backup de los ejercicios de producción
==========

Para traer los entregables, hacer en la máquina de producción: 

    $ sudo docker container ls
    $ sudo docker cp backend_container_id:/app/backend/media/zipped.tar.gz .

Y luego localmente

    $ scp site@10.10.0.215:thesis-desousa-wright/zipped.tar.gz .


