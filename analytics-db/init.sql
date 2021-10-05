CREATE USER shore_analytics WITH PASSWORD 'secret';
CREATE DATABASE shore_analytics WITH OWNER = shore_analytics;
ALTER USER shore_analytics CREATEDB;