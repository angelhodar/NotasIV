Docker
======

En esta sección se documentará la creación de un contenedor de docker para correr nuestra aplicación
de forma completamente aislada y solo con las dependencias estrictamente necesarias. Posteriormente,
se creará un repositorio en DockerHub con la imagen creada y se usará para desplegar en Heroku y Azure.

Creación de la imagen
---------------------

Para crear la imagen necesitamos crear 2 archivos:

* ``Dockerfile``: Contiene los comandos que se usarán para crear la imagen.
* ``.dockerignore``: Funciona como un .gitignore, nos permite indicar qué archivos
  queremos que no se añadan a nuestra imagen ya que son innecesarios (por ejemplo el directorio **.git**).

El archivo Dockerfile está documentado paso por paso y contiene lo siguiente:

.. code:: bash

    # Usamos la versión alpine de la versión 3.7 de python yaa que es
    # mucho mas ligera (100MB vs 1GB)
    FROM python:3.7-alpine

    # Exponemos el puerto 5000 que usará la app
    EXPOSE 5000

    # Copiamos primero solo el requirements para aprovecharnos del sistema
    # de layers de las imagenes docker e instalamos las dependencias
    COPY requirements.txt /tmp
    RUN cd /tmp && pip install -r requirements.txt

    # Copiamos los archivos (solo los no añadidos en el .dockerignore)
    COPY . /app
    # Nos movemos al directorio creado previamente.
    WORKDIR /app

    # Finalmente ejecutamos la app escuchando en el puerto 5000
    CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

Una vez tenemos el ``Dockerfile`` creado, debemos situarnos en el mismo directorio y ejecutar:

.. code:: bash

    # Esto creará una imagen llamada 'notas-iv', indicando con '.' el path donde está nuestro Dockerfile.
    $ docker build -t notas-iv .

Para listar las imagenes que tenemos creadas podemos ejecutar:

.. code:: bash

    $ docker images
    REPOSITORY            TAG                 IMAGE ID            CREATED             SIZE
    notas-iv              latest              0287ab292cdb        20 minutes ago      126MB

Para comprobar que la imagen funciona como debe, simplemente debemos arrancar un contenedor de esa imagen.
Para ello, simplemente ejecutamos:

.. code:: bash

    # -p le indica que vamos a mapear el puerto 5000 del anfitrión al puerto 5000 del contenedor.
    # Necesario ya que nuestra app escucha en el puerto 5000.
    $ docker run -p 5000:5000 notas-iv

Si accedemos a 127.0.0.1:5000 vemos que el contenedor funciona correctamente.

Docker Hub
----------

Ahora que ya tenemos nuestra imagen creada y funcionando, vamos a desplegarla en Docker Hub. Para ello primero nos registramos,
y cuando lo hayamos hecho le damos al boton **Create Repository** en en apartado de **Repositories**. Para automatizar la actualizacion
de la imagen cada vez que hagamos un push a nuestro repositorio, Docker Hub nos da directamente la opción de enganchar un repositorio de
GitHub desde donde obtener los datos para construir la imagen.

.. image:: images/dockerhub.png

Si queremos que Docker Hub obtenga la información necesaria desde el repositorio de GitHub que le hemos asignado,
deberemos darle a **Create & Build**. Si por el contrario queremos subir la imagen manualmente, le damos a **Create**.

Si elegimos la segunda opción, debemos ejecutar tan solo 3 comandos para subir la imagen a Docker Hub:

.. code:: bash

    # Nos logueamos a nuestra cuenta de Docker Hub
    $ docker login
    # Cambiamos el nombre de la imagen con el del repo, añadiendo el tag que queramos.
    $ docker tag notas-iv angelhodar/notas-iv:latest
    # Sube la imagen al repo remoto.
    $ docker push angelhodar/notas-iv:latest



    



