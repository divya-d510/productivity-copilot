#!/bin/bash
# Script to initialize the database schema

INSTANCE_CONNECTION_NAME="mapa-492317:asia-south1:productivity-db"
DB_USER="productivity_user"
DB_PASSWORD="AppPassword456!"
DB_NAME="productivity_db"

# Install PostgreSQL client
apt-get update && apt-get install -y postgresql-client

# Run schema
PGPASSWORD=$DB_PASSWORD psql \
  -h /cloudsql/$INSTANCE_CONNECTION_NAME \
  -U $DB_USER \
  -d $DB_NAME \
  -f /app/schema.sql

echo "Database initialized successfully"
