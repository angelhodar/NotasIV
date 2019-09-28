# NotasIV

## ¿En qué consiste este repositorio?

En este repositorio se pretende crear un micro-servicio que permita una fácil gestión de las notas de la asignatura IV para
los profesores que la imparten.

## ¿Cuál es la idea?

La idea es facilitar a los profesores la comunicación de las notas de cada practica de la asginatura a los estudiantes,
ya sea a través de un bot de Telegram o con otro cliente distinto, de forma individual a cada uno y a demanda por cada
estudiante, favoreciendo la privacidad en lugar de tener una hoja pública con la nota de todos los estudiantes.  

## Herramientas

* **Lenguaje**: Se programará en **Python** debido a su facilidad de uso y cantidad de librerias disponibles, permitiendo un mayor foco en la infraestructura que en las peculiaridades del lenguaje. En concreto se usará la versión **3.6.8**, ya que es estable pero no la última disponible, por lo que se pueden hacer pruebas de actualizar el entorno virtual y resolver posibles problemas de compatibilidad que se presenten.

* **Framework Web**: Para interactuar con el microservicio se usará una API REST, por lo que utilizaré el famoso microframewok [Flask](https://palletsprojects.com/p/flask/) para el desarrollo del apartado web, en concreto una extensión de la libreria llamada [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) que facilita la creación y el uso de buenas prácticas para la creación de la misma.

* **Tests**: Python dispone de varias librerias de testing. Las mas famosas son *unittest* (standard library), *nose* y *pytest*. De entre ellas he elegido **pytest** debido a la cantidad de extensiones (315+, como por ejemplo para [coverage](https://pypi.org/project/pytest-cov/)), facilidad de uso y perfecta retrocompatibilidad con las otras librerias mencionadas.

* **Almacenamiento**: Para almacenar los datos, he optado por utilizar **NoSQL**, en concreto **MongoDB** junto con el ORM [mongoengine](http://mongoengine.org/). He optado por esta vía porque a finales de verano estuve probando a usarlo en un proyecto y lo encontré muy facil de usar y gestionar, a la vez que me sirve para aprender nuevas tecnologías ya que yo al menos en cursos pasados de la carrera solo he dado SQL.

* **Logs**: En principio, usaré la librería [loguru](https://github.com/Delgan/loguru), la cual es una abstracción y mejora de la librería logging que viene incorporada en la standard library de python y que, según su autor, pretende mitigar los inconvenientes de la misma. Luego se integrará con el [Elastic Stack](https://www.elastic.co/es/what-is/elk-stack) para poder visualizar los logs comodamente a través de un dashboard (tengo que investigar mas de esto).

* **CI**: Para mantener un flujo de trabajo de integración continua, optaré por el uso de Travis CI dada su popularidad, aunque aun no he investigado mucho lo que ofrecen otros servicios como CircleCI como para decantarme por Travis al 100%.
