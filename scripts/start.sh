#!/bin/sh

echo "Waiting for database to be ready..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "Database is ready."

echo "Running Alembic migrations..."
poetry run alembic upgrade head

echo "Starting FastAPI app..."
exec poetry run python src/main.py
