#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status

# Check if the .env file exists and create it from the example if it doesn't
if [ ! -f /app/.env ]; then
  cp .env.example .env
fi

# Load environment variables from .env
if [ -f /app/.env ]; then
  . /app/.env
fi

# Function to wait until PostgreSQL is ready
wait_for_postgres() {
  until pg_isready -h db -p 5432 -U "$POSTGRES_USER"; do
    sleep 1
  done
}

wait_for_postgres

# Check if the database has been initialized (if alembic_version table exists)
export PGPASSWORD=$POSTGRES_PASSWORD

if psql -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1 FROM alembic_version LIMIT 1;" > /dev/null 2>&1; then
  echo "Database $POSTGRES_DB is already initialized. Skipping initialization."
else
  echo "Initializing and populating database..."
  alembic -c /app/vocabulary_builder/db/alembic.ini upgrade head
  python3.10 -m vocabulary_builder.db.db_populate /app/tiny_db_input.json
fi

unset PGPASSWORD

# Start the main process
exec "$@"
