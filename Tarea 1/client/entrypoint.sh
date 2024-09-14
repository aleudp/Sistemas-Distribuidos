#!/bin/bash

# Inicia el servicio de PostgreSQL
service postgresql start

# Espera a que PostgreSQL se inicie
sleep 5

# Configura la base de datos, crea la tabla e importa el CSV
psql -U postgres -d domains_db -f /docker-entrypoint-initdb.d/init_csv_table.sql

# Ejecuta el generador de tráfico (client.py)
python3 client.py

