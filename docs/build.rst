Construcción
============

Como herramienta de construcción se ha usado un ``Makefile`` ubicado en la raíz del proyecto, que contiene el siguiente codigo:

.. code:: bash

    .PHONY: tests docs clean
    init:
        pip install pipenv
        pipenv install --dev
    pm2:
        sudo apt update
        sudo apt install -y nodejs
        sudo apt install -y npm
        sudo npm install -g pm2
    tests:
        pipenv run python -m pytest -p no:warnings --cov-report=xml --cov=notas tests/
    coverage:
        pipenv run codecov
    docs:
        cd docs && pipenv run make html
    start:
        pipenv run pm2 start "gunicorn -b 0.0.0.0:$(PORT) app:app" --name app
    start-no-pm2:
        pipenv run gunicorn -b 0.0.0.0:$(PORT) app:app
    stop:
        pipenv run pm2 stop app
    delete:
        pipenv run pm2 delete app
    restart:
        pipenv run pm2 restart app
    heroku:
        sudo snap install heroku --classic
        heroku login
        heroku create notas-iv --buildpack heroku/python
        git push heroku master
    heroku-docker:
        sudo snap install heroku --classic
        heroku login
        heroku create notas-iv
        heroku stack:set container
        git push heroku master
    docker-build:
        docker build -t notas-iv .
    docker-run: docker-build
        docker run -e PORT=$(PORT) -p 5000:$(PORT) notas-iv
    vm:
        vagrant up --no-provision
    provision:
        vagrant provision
    clean:
        rm -f coverage.xml .coverage
        cd docs && make clean


A continuación se explica el funcionamiento de cada regla:

* ``init``: Instala el gestor de paquetes y entorno virtual `pipenv <https://pipenv-es.readthedocs.io>`_, a la vez que instala las dependencias del proyecto.
* ``pm2``: Instala npm y el paquete pm2.
* ``tests``: Ejecuta los tests y genera un reporte en formato xml.
* ``coverage``: Utiliza el reporte generado previamente para actualizar la página en `codecov.io <https://codecov.io/gh/angelhodar/NotasIV>`_
* ``docs``: Compila la documentación generando un directorio ``docs/_build`` con los archivos html para abrirlos con un navegador web.
* ``start``: Inicializa un contenedor de pm2 con un servidor WSGI.
* ``start-no-pm2``: Inicializa un servidor web WSGI sin usar pm2.
* ``stop``: Para el proceso de pm2 (pero no lo borra de memoria). Si se ejecuta ``start`` posteriormente se reactiva ese proceso parado.
* ``delete``: Para el proceso de pm2 y también lo borra de memoria.
* ``restart``: Reinicia el proceso de pm2.
* ``heroku``: Lleva a cabo todo lo necesario para desplegar la aplicación en Heroku. Para mayor información consulta la sección :doc:`./despliegue`
* ``heroku-docker``: Lleva a cabo todo lo necesario para desplegar la aplicación en Heroku usando docker. Para mayor información consulta la sección :doc:`./docker`
* ``docker-build: Crea una imagen de docker usando el ``Dockerfile``.
* ``docker-run``: Ejecuta un contenedor con nuestra imagen (si no está creada la crea en ese momento).
* ``vm``: Crea una máquina virtual con Vagrant. Para más información consulta la sección :doc:`./vagrant`
* ``provision``: Aprovisiona la máquina virtual creada previamente. Para más información consulta la sección :doc:`./vagrant`
* ``clean``: Limpia los archivos generados para codecov (útil para cuando se ejecutan en local y no en Travis por ejemplo).

Hay una directiva extra llamada ``.PHONY`` que evita confundir reglas con directorios existentes, como por ejemplo los tests.
Para ejecutar la herramienta de construcción con los tests simplemente debemos hacer lo siguiente:

.. code:: bash

    $ make
    $ make tests
