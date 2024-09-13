# Usar una imagen de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Copiar el archivo de requerimientos
COPY requirements.txt ./
# Agregar dnsutils para usar dig
RUN apt-get update && apt-get install -y dnsutils

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Ejecutar el servidor gRPC
CMD ["python3", "-u", "server.py"]
