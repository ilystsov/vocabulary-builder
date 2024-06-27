#!/bin/sh

cp .env.example .env

mkdir -p /app

if [ ! -f /app/test.db ]; then
  echo "Creating and populating database..."
  alembic -c /app/vocabulary_builder/db/alembic.ini upgrade head
  python3.10 -m vocabulary_builder.db.db_populate /app/tiny_db_input.json
else
  echo "Database already exists. Skipping creation."
fi

exec "$@"
