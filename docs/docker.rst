Docker
======

En esta sección se documentará la creación de un contenedor de docker para correr nuestra aplicación
de forma completamente aislada y solo con las dependencias estrictamente necesarias. Posteriormente,
se creará un repositorio en Docker Hub con la imagen creada y se usará para desplegar en Heroku y Azure.

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

    # Datos propios
    LABEL maintainer="Ángel Hódar (angelhodar76@gmail.com)"

    # Exponemos el puerto de la variable de entorno
    EXPOSE $PORT

    # Copiamos primero solo el requirements para aprovecharnos del sistema
    # de layers de las imagenes docker e instalamos las dependencias
    COPY requirements.txt /tmp
    RUN cd /tmp && pip install -r requirements.txt

    # Copiamos los archivos (solo los no añadidos en el .dockerignore)
    COPY . /app
    # Nos movemos al directorio creado previamente.
    WORKDIR /app

    # Finalmente ejecutamos la app escuchando en el puerto definido en PORT
    CMD gunicorn -b 0.0.0.0:${PORT} app:app

Una vez tenemos el ``Dockerfile`` creado, debemos situarnos en el mismo directorio y ejecutar:

.. code:: bash

    $ docker build -t notas-iv .

    Sending build context to Docker daemon  97.28kB
    Step 1/7 : FROM python:3.7-alpine
    ---> 8922d588eec6
    Step 2/7 : EXPOSE $PORT
    ---> Using cache
    ---> 82303a8b75d2
    Step 3/7 : COPY requirements.txt /tmp
    ---> Using cache
    ---> 2027a0d77ead
    Step 4/7 : RUN cd /tmp && pip install -r requirements.txt
    ---> Using cache
    ---> 90833d40b7ba
    Step 5/7 : COPY . /app
    ---> Using cache
    ---> 17725ae98b9b
    Step 6/7 : WORKDIR /app
    ---> Using cache
    ---> dc00b49afebb
    Step 7/7 : CMD gunicorn -b 0.0.0.0:${PORT} app:app
    ---> Using cache
    ---> 2a90f78a4ae6
    Successfully built 2a90f78a4ae6
    Successfully tagged notas-iv:latest

Esto creará una imagen llamada **notas-iv**, indicando con **.** el path donde está nuestro Dockerfile.
En este caso como ya se ha ejecutado previamente, vemos como usa la caché para no tener que ejecutar
cada comando de nuevo. Esto es especialmente interesante en el caso de la instalación de dependencias
con **pip**, ya que solo se ejecutará si cambiamos alguna dependencia, en lugar de hacerse siempre que
hagamos un cambio en el código por ejemplo.

Para listar las imagenes que tenemos creadas podemos ejecutar:

.. code:: bash

    $ docker images

    REPOSITORY            TAG                 IMAGE ID            CREATED             SIZE
    notas-iv              latest              0287ab292cdb        20 minutes ago      126MB

Para comprobar que la imagen funciona como debe, simplemente debemos arrancar un contenedor de esa imagen.
Para ello, simplemente ejecutamos:

.. code:: bash

    $ docker run -e PORT=$PORT -p $HOST_PORT:$PORT notas-iv

    [2019-11-21 15:04:40 +0000] [1] [INFO] Starting gunicorn 19.9.0
    [2019-11-21 15:04:40 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
    [2019-11-21 15:04:40 +0000] [1] [INFO] Using worker: sync
    [2019-11-21 15:04:40 +0000] [7] [INFO] Booting worker with pid: 7


La opción ``-p`` le indica que vamos a mapear el puerto ``$HOST_PORT`` del anfitrión al puerto ``$PORT`` del contenedor.
Basicamente esto quiere decir que si queremos acceder a nuestro contenedor localmente en la dirección **127.0.0.1:550** por ejemplo,
el valor de ``$HOST_PORT`` debe de ser **550**, mientras que el valor de ``$PORT`` deberá de ser aquel en el que queremos que escuche
nuestra app web dentro de su contenedor (en el caso de la ejecución anterior era **5000**).

Además, con la opción ``-e`` hacemos que el servidor WSGI de Gunicorn se ejecute escuchando en el puerto definido en la variable
de entorno ``$PORT`` mencionada anteriormente, algo necesario también posteriormente cuando se ejecuta en Heroku.

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

Ahora necesitamos un paso extra para automatizar las builds con GitHub, ya que si seleccionamos **Create & Build**
solo se crea en ese momento, pero no se tienen en cuenta futuros ``git push`` que se hagan en el repo.

En nuestro repositorio de Docker Hub, debemos irnos al apartado Builds y configurarlo de esta manera:

.. image:: images/dockerhub_build.png

Una vez lo hayamos hecho, le damos al botón **Save and Build** y se iniciará una nueva build de nuestra imagen.
Cuando se complete nos deberá salir un resultado tal que asi:

.. image:: images/dockerhub_build_success.png

Y con esto ya tendriamos Docker Hub completamente configurado y automatizado con nuestro repo de GitHub.

Depligue en Heroku
------------------

Una vez tenemos la imagen en Docker Hub, estamos listos para poder desplegar el contenedor
en distintos servicios. En este caso vamos a ver cómo desplegarlo en Heroku.

Para empezar, necesitamos estar logueados en Heroku desde el CLI, asi que ejecutamos:

.. code:: bash

    $ heroku login

Ahora creamos nuestra app con el nombre que queramos, en mi caso va a ser **notas-iv**.

.. code:: bash

    $ heroku create notas-iv

    Creating ⬢ notas-iv... done
    https://notas-iv.herokuapp.com/ | https://git.heroku.com/notas-iv.git

Una vez tenemos la app creada, necesitamos crear un archivo llamado ``heroku.yml``, que tendrá una funcionalidad
parecida al ``Procfile``, pero esta vez se encargará de monstar y correr la imagen que definamos en el Dockerfile
en la app que hemos creado previamente. El archivo tiene el siguiente formato:

.. code:: yaml

    build:
        docker:
            web: Dockerfile

Cuando lo tengamos listo simplemente hacemos un commit con el archivo a nuestro repo y cambiamos el stack de nuestra app
a modo contenedor con el siguiente comando:

.. code:: bash

    $ heroku stack:set container

Y ya solo falta hacer push de nuestra app a Heroku:

.. code:: bash

    $ git push heroku master

Otra forma:

Primero debemos logearnos en el container registry de Heroku:

.. code:: bash

    $ heroku container:login

En nuestro caso, como ya tenemos la imagen creada, debemos cambiarle el nombre de tal forma
que podamos subirla al container registry de Heroku:

.. code:: bash

    $ docker tag notas-iv registry.heroku.com/notas-iv/web

Ahora primero antes que nada debemos irnos a la web de Heroku y crear una app con el nombre que queramos,
en mi caso la he llamado igual que la imagen. 

.. Note:: También podríamos hacerlo desde el CLI ejecutando ``heroku create notas-iv``, pero nos desplegará la app usando el Procfile, cosa que no queremos ya que nos interesa hacerlo con un contenedor.

Una vez tenemos la app creada, ahora si, la subimos al registro de Heroku:

.. code:: bash

    $ docker push registry.heroku.com/notas-iv/web

Ahora tan solo nos queda desplegarlo en Heroku para poder acceder a él
desde una URL:

.. code:: bash

    $ heroku container:release web -a notas-iv


Despliegue en Azure
-------------------

Desplegar en Azure es tremendamente sencillo, tan solo debemos crear un nuevo App Service y especificarle que queremos usar un contenedor Docker:

(captura)

Y para configurarle la imagen que queremos, debemos seleccionar el proveedor de imagenes que queramos, en nuestro caso sería Docker Hub, especificandole
la ruta completa de nuestra imagen, con el nombre del repo y el tag que queremos usar:

(captura)




    



