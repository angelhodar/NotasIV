Construcción
============

Como herramienta de construcción se ha usado un ``Makefile`` ubicado en la raíz del proyecto, que contiene el siguiente codigo:

.. code:: bash

    .PHONY: tests clean
    init:
        pip install pipenv
        pipenv install --dev
    tests:
        pipenv run python -m pytest --cov-report=xml --cov=notas tests/
    coverage:
        codecov
    clean:
        rm coverage.xml .coverage

A continuación se explica el funcionamiento de cada regla:

* ``init``: Instala el gestor de paquetes y entorno virtual `pipenv <https://pipenv-es.readthedocs.io>`_, a la vez que instala las dependencias del proyecto.
* ``tests``: Ejecuta los tests y genera un reporte en formato xml.
* ``codecov``: Utiliza el reporte generado previamente para actualizar la página en `codecov.io <https://codecov.io/gh/angelhodar/NotasIV>`_
* ``clean``: Limpia los archivos generados para codecov (útil para cuando se ejecutan en local y no en Travis por ejemplo).

Hay una directiva extra llamada ``.PHONY`` que evita confundir reglas con directorios existentes, como por ejemplo los tests.
Para ejecutar la herramienta de construcción con los tests simplemente debemos hacer lo siguiente:

.. code:: bash

    $ make
    $ make tests
