#!/bin/bash

psql -U "${POSTGRES_USER}" -d "shore_analytics" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL
