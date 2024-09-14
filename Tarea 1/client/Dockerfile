# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt ./

# Instalar las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del cliente al directorio de trabajo en el contenedor
COPY . .

# Ejecutar el archivo client.py
CMD ["python3", "-u", "client.py"]

