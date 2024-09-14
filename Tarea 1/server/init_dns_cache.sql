CREATE TABLE IF NOT EXISTS dns_queries (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    ip_address VARCHAR(255) NOT NULL,
    partition_number INT,
    query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dns_traffic (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    ip_address VARCHAR(255),
    query_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cache_status VARCHAR(10) NOT NULL  -- 'HIT' o 'MISS'
);

CREATE TABLE IF NOT EXISTS dns_cache_stats (
    id SERIAL PRIMARY KEY,
    total_queries INT NOT NULL,
    hits INT NOT NULL,
    misses INT NOT NULL,
    calculation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

