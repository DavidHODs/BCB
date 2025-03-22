#!/bin/sh

echo "Waiting for database to be ready..."

echo "Database is ready."

echo "Running Alembic migrations..."
poetry run alembic upgrade head

echo "Starting FastAPI app..."
exec poetry run python src/main.py
