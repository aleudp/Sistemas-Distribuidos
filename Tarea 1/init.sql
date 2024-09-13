-- init.sql
CREATE TABLE IF NOT EXISTS dns_queries (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255),
    ip_address VARCHAR(255),
    query_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

