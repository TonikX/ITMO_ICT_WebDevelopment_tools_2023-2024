#!/bin/bash
set -e

# Start PostgreSQL service
pg_ctl -D "$PGDATA" -o "-c listen_addresses='localhost'" -w start

# Restore the database from the custom dump file
pg_restore -U postgres -d "$POSTGRES_DB" /docker-entrypoint-initdb.d/task_manager_empty.sql

# Stop PostgreSQL service
pg_ctl -D "$PGDATA" -m fast -w stop
