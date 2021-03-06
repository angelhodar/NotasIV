# NotasIV

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/angelhodar/NotasIV.svg?branch=master)](https://travis-ci.com/angelhodar/NotasIV)
[![CircleCI](https://circleci.com/gh/angelhodar/NotasIV.svg?style=svg)](https://circleci.com/gh/angelhodar/NotasIV)
[![codecov](https://codecov.io/gh/angelhodar/NotasIV/branch/master/graph/badge.svg)](https://codecov.io/gh/angelhodar/NotasIV)
[![Documentation Status](https://readthedocs.org/projects/notasiv/badge/?version=master)](https://notasiv.readthedocs.io/en/latest/?badge=master)

## ¿En qué consiste este repositorio?

En este repositorio se pretende crear un micro-servicio que permita una fácil gestión de las notas de la asignatura IV para
los profesores que la imparten.

## ¿Cuál es la idea?

La idea es facilitar a los profesores la comunicación de las notas de cada practica de la asginatura a los estudiantes,
ya sea a través de un bot de Telegram o con otro cliente distinto, de forma individual a cada uno y a demanda por cada
estudiante, favoreciendo la privacidad en lugar de tener una hoja pública con la nota de todos los estudiantes.  

## Documentacion

Toda la documentación que se vaya añadiendo sobre el microservicio se puede encontrar [aqui](https://notasiv.readthedocs.io/en/latest/index.html), aunque se puede ir directamente a la sección deseada a través del siguiente índice:

* [Herramientas](https://notasiv.readthedocs.io/en/latest/herramientas.html)
* [Build Tool](https://notasiv.readthedocs.io/en/latest/build.html)
* [Integración Continua](https://notasiv.readthedocs.io/en/latest/ci.html)
* [Clase](https://notasiv.readthedocs.io/en/latest/clase.html)
* [API](https://notasiv.readthedocs.io/en/latest/api.html)
* [Despliegue en un PaaS](https://notasiv.readthedocs.io/en/latest/despliegue.html)
* [Docker](https://notasiv.readthedocs.io/en/latest/docker.html)
* [Creación y aprovisionamiento](https://notasiv.readthedocs.io/en/latest/vagrant.html)
* [Despliegue de la VM en Azure](https://notasiv.readthedocs.io/en/latest/cloud_deploy.html)

### Herramienta de construccion
```
buildtool: Makefile
```

### App:
```
Despliegue: https://notas-iv.herokuapp.com/

Contenedor: https://notas-iv.azurewebsites.net/
```

### Docker Hub
```
URL: https://hub.docker.com/r/angelhodar/notas-iv
```
Para descargar y ejecutar la imagen localmente, tan solo se debe ejecutar lo siguiente:

```
docker pull angelhodar/notas-iv:latest
docker run -e PORT=$PORT -p $HOST_PORT:$PORT notas-iv .
```

### Aprovisionamiento
```
provision: provisioning/playbook.yml
```

### Despliegue de la VM en Azure

```
Despliegue final: 52.236.139.44:5000
```