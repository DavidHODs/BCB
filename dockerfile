FROM python:3.11 as builder

WORKDIR /

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-interaction --no-ansi

FROM python:3.11-slim

WORKDIR /

RUN apt-get update && apt-get install -y \
  libpq-dev \
  gcc \
  netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY --from=builder /.venv /.venv

ENV PATH="/.venv/bin:$PATH" \
  PYTHONPATH="/"

COPY . .

RUN chmod +x scripts/start.sh

EXPOSE 9000

ENTRYPOINT ["/scripts/start.sh"]
