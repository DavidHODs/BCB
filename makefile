install:
	poetry install

lint:
	poetry run autopep8 --aggressive --indent-size 2 --max-line-length 80 --in-place --recursive src/
	poetry run isort --line-length 80 --indent 2 src/
	poetry run ruff check --fix src/
	poetry run mypy src/ 

run:
	poetry run python src/main.py

