-- Crear la tabla para almacenar los dominios
CREATE TABLE IF NOT EXISTS domains (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255)
);

-- Cargar los datos desde el archivo CSV
COPY domains(domain)
FROM '/docker-entrypoint-initdb.d/3rd_lev_domains.csv'
DELIMITER ','
CSV HEADER;

