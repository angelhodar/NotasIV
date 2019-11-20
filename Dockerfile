# Usamos la versión alpine de 3.7 ya que es mucho mas ligera (100MB vs 1GB)
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
