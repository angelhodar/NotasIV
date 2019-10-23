Integración Continua
====================

Como sistemas de integración continua se han usado TravisCI y CircleCI.

TravisCI
--------

El sistema de Travis se configura únicamente con un archivo ``.travis.yml`` que debe
estar ubicado en la raiz de nuestro proyecto. Este archivo contiene la siguiente información:

.. code:: yaml

    language: python
    python:
      - "3.5"
      - "3.6"
      - "3.7"
      - "3.8"
      - "3.8-dev"
    install:
      - make
    script:
      - make tests
      - make start
      - make delete
    after_success:
      - make coverage

Simplemente le definimos el lenguaje de programación que vamos a usar, junto con las distintas versiones
del mismo con las que vamos a testear nuestra aplicación. Como dijimos en la sección anterior, para ejecutar
nuestra herramienta de construcción en el entorno que nos da travis simplemente debemos usar ``make`` para instalar todo
lo necesario para ejecutar nuestros tests y arrancar el microservicio. Por lo tanto, en la directiva ``script`` solo
debemos ejecutar ``make tests`` y ``make start``. Si todo ha ido bien, usando la directiva ``after_success`` se ejecutará
``make coverage`` para mandar los reportes generados en la ejecución de los tests a la plataforma `codecov.io <https://codecov.io/gh/angelhodar/NotasIV>`_.

CircleCI
--------

Para CircleCI la configuración es bastante similar, aunque se ha reducido la versión de python solo a la versión específica usada
en desarrollo local del proyecto. En este caso el archivo de configuración pasa a llamarse ``config.yml`` y hay
que ubircarlo en un directorio ``.circleci`` en la raiz de nuestro proyecto. El archivo ``config.yml`` contiene lo siguiente:

.. code:: yaml

    version: 2
  jobs:
    build:
      docker:
        - image: circleci/python:3.5
        - image: circleci/python:3.6
        - image: circleci/python:3.7
        - image: circleci/python:3.8
        - image: circleci/python:latest
      steps:
        # Obtenemos codigo del repo
        - checkout
        # Entorno virtual y dependencias
        - run:
            name: Entorno y dependencias
            command: |
              make
        # Ejecucion de los tests
        - run:
            name: Ejecutar tests
            command: |
              make tests
        # Actualiza codecov
        - run:
            name: Coverage
            command: |
              make coverage
        # Arranca el microservicio
        - run:
            name: Arranque 
            command: |
              make start
        # Para y borra el microservicio
        - run:
            name: Parada 
            command: |
              make delete


En este caso, aunque la configuración es menos trivial que con Travis, ya que por ejemplo para indicar la versión de python específica que queremos
debemos buscar cual es la imagen de docker que contiene exactamente la versión que queremos. Aun asi, realmente es bastante intuitivo, permitiendo múltiples configuraciones
y posibilidades.

