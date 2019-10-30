API
===

En esta sección se muestra la documentación de la API implementada con Swagger para no solo ver los
métodos que ofrece el microservicio, sino también para poder testearlo, así como la documentación de
cada función de los tests.

Swagger
-------

El paquete ``flask-restplus`` usado para el desarrollo de la API-RESTful, poniéndole una serie de decoradores
a los métodos, genera una documentación con Swagger que puede ser visualizada en el endpoint ``/`` de la API con Swagger UI
y muestra tanto los métodos disponibles como los modelos JSON devueltos por la API (aumenta el zoom en el navegador si no lo ves bien).

.. image:: images/swagger.png

Swagger UI también ofrece la posibilidad de probar la API cómodamente como si uśaramos Postman por ejemplo. Nos dice los outputs que ofrece
un endpoint y la posibilidad de hacer POST y PUT adjuntando cómodamente un JSON en el body de la petición. Para poder probar toda esta
funcionalidad, como ya tengo la app corriendo en Heroku, puedes acceder a ella simplemente haciendo click `aquí <https://notas-iv.herokuapp.com/>`_

Tests
-----

Toda la funcionalidad referente a los tests sobre la API la puedes encontrar en el archivo ``tests/tests_api.py``. A continuación
se muestra una breve documentación sobre cada método implementado.

.. autoapimodule:: test_api
    :members: test_status, test_get_students, test_post_student, test_get_student, test_put_student, test_delete_student