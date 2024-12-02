-- init_cassandra.cql

CREATE KEYSPACE IF NOT EXISTS waze_keyspace 
WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '1'};

USE waze_keyspace;

CREATE TABLE IF NOT EXISTS waze_incidents (
    id UUID PRIMARY KEY,
    type TEXT,
    position TEXT,
    timestamp TIMESTAMP,
    date TEXT,
    x_coordinate TEXT,
    y_coordinate TEXT,
    type_keywords LIST<TEXT>
);

DESCRIBE TABLE waze_keyspace.waze_incidents;

