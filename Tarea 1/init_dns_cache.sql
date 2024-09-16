CREATE TABLE IF NOT EXISTS dns_domain_data (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    ip_address VARCHAR(255),
    partition_number INT,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS dns_hit_miss (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    partition_number INT,
    result VARCHAR(4) NOT NULL CHECK (result IN ('HIT', 'MISS')),
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

