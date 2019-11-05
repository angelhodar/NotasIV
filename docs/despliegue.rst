Despliegue en un PaaS
=====================

Heroku
------

La primera opción de PaaS que se ha usado es Heroku debido a su simpleza de uso para ir familiarizandome con despliegues.
Para configurar un despliegue desde la herramienta de construcción, se ha incluido la regla ``make heroku`` en el
``Makefile``. Esta regla contiene las siguientes acciones:

1. ``sudo snap install heroku --classic``: Instala el CLI de Heroku en Ubuntu con el gestor de paquetes **snap**.
2. ``heroku login``: Abre el navegador y nos pide introducir nuestros credenciales de Heroku para loguearnos en el CLI.
3. ``heroku create notas-iv --buildpack heroku/python``: Crea nuestra aplicación con nombre **notas-iv** con el buildpack
   de python que ofrece Heroku (aunque no era realmente necesario incluirlo ya que Heroku detecta el lenguaje de la app
   automaticamente), enlazando un repostiorio remoto a nuestro repositorio local.
4. ``git push heroku master``: Desplegamos nuestra aplicación en el repositorio remoto creado anteriormente.

Para saber cómo debe Heroku ejecutar nuestra aplicación, es necesario incluir un archivo llamado ``Procfile`` en la raiz
del proyecto con el siguiente contenido:

.. code:: bash

    web: make start-no-pm2

Debemos de poner el keyword ``web`` para decirle a Heroku que nuestra aplicación es un servicio web que recibirá peticiones
HTTP y nos habilita un puerto que deberemos asignar a nuestra aplicación con la variable de entorno ``$PORT``. Se ha creado una
regla ``start-no-pm2`` ya que no tiene sentido ejecutar nuestra aplicación en pm2 si ya el propio Heroku nos proporciona las
herramientas necesarias, como la escalabilidad por ejemplo.

Heroku y GitHub
***************

Cuando ya tenemos la aplicación desplegada, cada vez que hagamos un push a nuestro repo debemos de ejecutar
``git push heroku master`` para notificar a Heroku de los cambios y que actualice nuestra aplicación. Para
evitar esto, podemos configurar el repo de GitHub de nuestra aplicación para que cada vez que hagamos un push
a nuestro repo, automaticamente Heroku actualice la aplicación. 

Para ello simplemente debemos irnos al apartado **Desploy** en la página de nuestra aplicación en Heroku y
en el apartado *Deployment method* le damos a GitHub e introducimos nuestros credenciales de Github. AHora solo
faltaría seleccionar el repo correspondiente a la aplicación.

Esto crea un hook en nuestro repo que se enlazará con Heroku cada vez que se introduzca un cambio. También nos da
la posibilidad de configurar si queremos que ese nuevo despliegue solo se lleve a cabo si la nueva versión de nuestro
repo pasa los tests en el CI que tengamos configurado en caso de tener alguno, sin necesidad de configurar nada mas.

En la siguiente imagen se puede ver como queda todo configurado despues de terminar el proceso:

.. image:: images/heroku-github.png

Ahora simplemnete cada vez que incluyamos un cambio en nuestro repo, Heroku ya se encargará de actualizar nuestra app
(siempre y cuando pase los tests correspondientes).