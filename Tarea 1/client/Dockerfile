# Usar una imagen de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Copiar el archivo de requerimientos
COPY requirements.txt ./

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Ejecutar el cliente que genera tráfico
CMD ["python3", "-u", "client.py"]
