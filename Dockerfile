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
