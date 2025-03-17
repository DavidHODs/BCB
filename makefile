install:
	poetry install

pre-commit-install:
	poetry run pre-commit install

pre-commit-run:
	poetry run pre-commit run --all-files

lint:
	poetry run black .
	poetry run isort .
	poetry run mypy .

run:
	poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

