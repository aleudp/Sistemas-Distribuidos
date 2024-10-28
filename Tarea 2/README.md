# Sistemas Distribuidos - Tarea 2

Este proyecto implementa un sistema distribuido con Kafka, gRPC, y Elasticsearch, diseñado para procesar y monitorear datos en tiempo real.

## Requisitos Previos

- **Kafka**: Asegúrate de tener Kafka instalado y configurado.
- **gRPC Tools**: Debes tener las herramientas gRPC instaladas para compilar los servicios gRPC necesarios.

## Pasos para Configurar y Ejecutar el Proyecto

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/ale_udp/Sistemas_Distribuidos.git
   cd Sistemas_Distribuidos/Tarea\ 2
   ```
2. **Generar los conjuntos de datos**
Desde la carpeta raíz del proyecto, ejecuta el script dataset.py para crear los tres datasets que utilizará el sistema.
```bash
python dataset.py
```
3. **Construir y levantar los contenedoresConstruir y levantar los contenedores**
Ejecuta los siguientes comandos desde la carpeta raíz para construir y levantar todos los servicios en contenedores Docker:
   ```bash
   docker compose build
   docker compose up -d
   ```



