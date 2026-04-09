#!/bin/bash
set -e

echo "Initializing database schema..."

# Use Cloud SQL connection
export PGPASSWORD="${DB_PASSWORD}"

psql -h 127.0.0.1 -U "${DB_USER}" -d "${DB_NAME}" -f /schema.sql

echo "Database schema initialized successfully!"
