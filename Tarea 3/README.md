# Tarea 3 - Sistemas Distribuidos

Este proyecto utiliza Docker Compose, Kafka, Spark, Cassandra y Elasticsearch para procesar datos extraídos de Waze mediante scrapping.

## Pasos para correr el proyecto

1. **Clonar el repositorio**  
   Descarga el repositorio desde GitHub ejecutando el siguiente comando:
   ```bash
   git clone https://github.com/aleudp/Sistemas-Distribuidos.git

2. **Navegar a la carpeta del proyecto**  
   Ve a la ruta de la carpeta donde se descargó el proyecto:
   ```bash
   cd Sistemas-Distribuidos/Tarea\ 3

3. **Construir los contenedores**  
   Ejecuta el siguiente comando para construir las imágenes de Docker:
   ```bash
   docker compose build
   
4. **Levantar los contenedores**  
   Inicia los servicios definidos en el archivo docker-compose.yml:
   ```bash
   docker compose up
   
5. **Acceder al contenedor de Spark**  
   Una vez que los contenedores estén levantados, entra al contenedor de Spark ejecutando:
   ```bash
   docker exec -it spark /bin/bash

7. **Ejecutar el script de Spark**  
   Dentro del contenedor, ejecuta el script de Spark para procesar los datos:
   ```bash
   python3 spark.py

8. **Visualizar las interfaces de usuario**  
   Puedes acceder a las interfaces de usuario en los siguientes enlaces:
   ```bash
   Kibana: http://localhost:5601
   Kafka: http://localhost:8083
