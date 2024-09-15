# Usar una imagen ligera de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Copiar el archivo de requerimientos
COPY requirements.txt ./

# Actualizar el sistema e instalar las dependencias necesarias (dnsutils para DIG)
RUN apt-get update && apt-get install -y dnsutils && rm -rf /var/lib/apt/lists/*

# Instalar las dependencias necesarias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del servidor
COPY . .

# Exponer el puerto del servidor gRPC
EXPOSE 50051

# ENTRYPOINT ["/usr/src/app/wait-for-it.sh", "postgres:5432", "--", "python3", "server.py"]

# Ejecutar el servidor gRPC
CMD ["python3", "-u", "server.py"]

