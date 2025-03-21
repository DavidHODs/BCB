MIGRATIONS_DIR=src/database/migrations


install:
	poetry install

lint:
	poetry run autopep8 --aggressive --indent-size 2 --max-line-length 80 --in-place --recursive src/
	poetry run isort --line-length 80 --indent 2 src/
	poetry run ruff check --fix src/
	poetry run mypy src/ 

run:
	poetry run python src/main.py

init-db:
	@alembic init $(MIGRATIONS_DIR)

makemigration:
	@if [ -z "$(NAME)" ]; then echo "Error: NAME is required. Usage: make migrate NAME='your_migration_name'"; exit 1; fi
	@alembic revision -m "$(NAME)"

migrate:
	@alembic upgrade head

downgrade:
	@alembic downgrade -1

db-history:
	@alembic history

db-current:
	@alembic current

db-stamp:
	@alembic stamp head