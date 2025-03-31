#!/bin/sh

echo "Running Alembic migrations..."
poetry run alembic upgrade head

echo "Starting FastAPI app..."
exec poetry run python src/main.py
