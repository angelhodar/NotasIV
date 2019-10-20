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
        codecov
    docs:
        cd docs && make html
    start:
        touch tmp.pid
        pipenv run uwsgi --http 127.0.0.1:5000 --module app:app --master --processes 4 --threads 2 --safe-pidfile tmp.pid
    stop:
        pipenv run uwsgi --stop tmp.pid
    reload:
        pipenv run uwsgi --reload tmp.pid
    clean:
        rm coverage.xml .coverage
        cd docs && make clean

A continuación se explica el funcionamiento de cada regla:

* ``init``: Instala el gestor de paquetes y entorno virtual `pipenv <https://pipenv-es.readthedocs.io>`_, a la vez que instala las dependencias del proyecto.
* ``tests``: Ejecuta los tests y genera un reporte en formato xml.
* ``coverage``: Utiliza el reporte generado previamente para actualizar la página en `codecov.io <https://codecov.io/gh/angelhodar/NotasIV>`_
* ``docs``: Compila la documentación generando un directorio ``docs/_build`` con los archivos html para abrirlos con un navegador web.
* ``start``: Inicitaliza un contenedor WSGI con 4 procesos y 2 hilos cada uno, guardando el pid del proceso master necesario para ``stop`` y ``reload``.
* ``stop``: Finaliza el contenedor WSGI de la `manera conveniente <https://uwsgi-docs.readthedocs.io/en/latest/Management.html>`_, en lugar de matando el proceso con señales al SO.
* ``reload``: Reinicia los workers del contenedor WSGI, de nuevo con la manera conveniente.
* ``clean``: Limpia los archivos generados para codecov (útil para cuando se ejecutan en local y no en Travis por ejemplo).

Hay una directiva extra llamada ``.PHONY`` que evita confundir reglas con directorios existentes, como por ejemplo los tests.
Para ejecutar la herramienta de construcción con los tests simplemente debemos hacer lo siguiente:

.. code:: bash

    $ make
    $ make tests
