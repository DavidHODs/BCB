install:
	poetry install

pre-commit-install:
	poetry run pre-commit install

pre-commit-run:
	poetry run pre-commit run --all-files

lint:
	poetry run autopep8 --aggressive --indent-size 2 --max-line-length 80 --in-place --recursive .
	poetry run isort --line-length 80 --indent 2 .
	poetry run mypy .



run:
	poetry run python src/main.py

