# Sistemas Distribuidos - Tarea 2

Este proyecto implementa un sistema distribuido con Kafka, gRPC, y Elasticsearch, diseñado para procesar y monitorear datos en tiempo real, simulando ventas de productos online.

## Requisitos Previos

- **Kafka**: Asegúrate de tener Kafka instalado y configurado.
- **gRPC Tools**: Debes tener las herramientas gRPC instaladas para compilar los servicios gRPC necesarios.

## Pasos para Configurar y Ejecutar el Proyecto:

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/ale_udp/Sistemas_Distribuidos.git
   cd Sistemas_Distribuidos/Tarea\ 2
   ```
2. **Generar los conjuntos de datos**:
    Desde la carpeta raíz del proyecto, ejecuta el script dataset.py para crear los tres datasets que utilizará el sistema.
```bash
python dataset.py
```
3. **Construir y levantar los contenedores**: 
    Ejecuta los siguientes comandos desde la carpeta raíz para construir y levantar todos los servicios en contenedores Docker:
   ```bash
   docker compose build
   docker compose up -d
   ```
4. **Acceder a las interfaces web**:
    Kafka UI: Accede a http://localhost:8080 para ver la interfaz de Kafka y monitorear los tópicos.
   Kibana (Elasticsearch UI): Accede a http://localhost:5601 para ver los datos en Elasticsearch.
   
5. **Ejecutar los servicios individuales**:
    En diferentes terminales, navega a las carpetas y ejecuta cada servicio de la siguiente manera:
      gRPC Server:
      ```bash
      cd grpc_server
      python grpc_server.py
      ```
      State Machine:
      ```bash
      cd state-machine
      python state_machine.py
      ```
      Elastic Ingest Service:
      ```bash
      cd elastic
      python elastic.py
      ```
      Notification Service:
      ```bash
      cd notification_service
      python notification_service.py
      ```
6. **Inyectar datos a través del gRPC Client**:
     Finalmente, desde otra terminal, navega a la carpeta grpc_server y ejecuta el cliente gRPC para comenzar a inyectar datos:
   ```bash
   cd grpc_server
   python grpc_client.py
   ```
