#!/bin/bash

psql -U "${POSTGRES_USER}" -d "shore" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL
