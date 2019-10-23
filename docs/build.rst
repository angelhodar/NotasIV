Construcción
============

Como herramienta de construcción se ha usado un ``Makefile`` ubicado en la raíz del proyecto, que contiene el siguiente codigo:

.. code:: bash

    .PHONY: tests docs clean
    init:
        pip install pipenv
        pipenv install --dev
    tests:
        pipenv run python -m pytest -p no:warnings --cov-report=xml --cov=notas tests/
    coverage:
        pipenv run codecov
    docs:
        cd docs && make html
    start:
        sudo apt install npm
	    sudo npm install -g pm2
        pipenv run pm2 start "uwsgi --http 127.0.0.1:5000 --module app:app --master --processes 4 --threads 2" --name app
    stop:
        pipenv run pm2 stop app
    delete:
        pipenv run pm2 delete app
    restart:
        pipenv run pm2 restart app
    clean:
        rm coverage.xml .coverage
        cd docs && make clean

A continuación se explica el funcionamiento de cada regla:

* ``init``: Instala el gestor de paquetes y entorno virtual `pipenv <https://pipenv-es.readthedocs.io>`_, a la vez que instala las dependencias del proyecto.
* ``tests``: Ejecuta los tests y genera un reporte en formato xml.
* ``coverage``: Utiliza el reporte generado previamente para actualizar la página en `codecov.io <https://codecov.io/gh/angelhodar/NotasIV>`_
* ``docs``: Compila la documentación generando un directorio ``docs/_build`` con los archivos html para abrirlos con un navegador web.
* ``start``: Instala e inicializa un contenedor de pm2 usando WSGI con 4 procesos y 2 hilos cada uno dentro del mismo.
* ``stop``: Para el proceso de pm2 (pero no lo borra de memoria). Si se ejecuta ``start`` posteriormente se reactiva ese proceso parado.
* ``delete``: Para el proceso de pm2 y también lo borra de memoria.
* ``restart``: Reinicia el proceso de pm2.
* ``clean``: Limpia los archivos generados para codecov (útil para cuando se ejecutan en local y no en Travis por ejemplo).

Hay una directiva extra llamada ``.PHONY`` que evita confundir reglas con directorios existentes, como por ejemplo los tests.
Para ejecutar la herramienta de construcción con los tests simplemente debemos hacer lo siguiente:

.. code:: bash

    $ make
    $ make tests
