# Frontend

## Preview and development

1- Clone this repository
```javascript
git clone https://github.com/thesis-desousa-wright/frontend.git
cd frontend
```

2- Install dependencies
```javascript
npm i 
```

3- Run app in development mode
```javascript
npm start
```

## Test

In order to launch the test runner in interactive watch mode run
```javascript
npm test
```

## Build

```javascript
npm run build
```

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

## Actualizar material

### Contenido

Para actualizar el contenido de la materia, se deben editar, agregar o modificar los archivos dentro de la carpeta `public/content`. Ahi se encuentran las carpetas de las unidades con sus respectivos archivos. 

Consideraciones:

Las rutas no corresponden a como esta organizado el contenido en la carpeta `public/content` sino a las rutas definitas en `src/content/content.json` (+ info sobre rutas en la sección siguiente)

Por ejemplo: Sea un archivo cualquiera, en el que se quiere agregar un link al siguiente archivo `public/content/01_Introduccion/06_CierreClase.md`. Para lograr eso, vamos a ir al archivo de rutas y ver la ruta asignada a ese archivo:

```
{
  ...
  "units": {
    "introduccion": {
      ....
      "cierre-de-clase": {
        "title": "1.6 Cierre de la clase",
        "file": "/content/01_Introduccion/06_CierreClase.md",
        "isPrivate": true
      }
    }
```

entonces el link que pondremos en el archivos sera `/programa/units/introduccion/cierre-de-clase`

### Rutas

Una vez que el contenido esta listo, se pueden actualizar las rutas en el siguiente archivo `src/content/content.json`.

La estructura del mismo es la siguiente:

```
{
  title: string
  isPrivate: boolean
  file?: string
  [key: string]: Section
  date?: string //YYYY-MM-DD
}
```

donde 
- title es usado como label en la NavBar
- isPrivate esconde secciones si el usuario no esta loggeado
- file es la ruta donde el archivo que tiene el markdown esta ubicado (por ejemplo e.g. /content/01_Introduccion/06_CierreClase.md)
- date guarda la fecha en que el contenido estar disponible/visible para los alumnos
- keys si el file es una carpeta, se pueden anidar mas de estos objetos para representar los archivos que contiene 