# FastAPI Learning Project – Book Club API

This project is a structured learning exercise to explore **FastAPI** while reinforcing backend and DevOps principles. As a backend + devops engineer, the goal is to understand FastAPI’s architecture, request handling, async capabilities, and its comparison to other backend frameworks.

## Overview

This API simulates a **Book Club** where users can:

- Search for books summary locally and externally via Gutendex API.
- Engage in discussion threads related to books via chat.

## Features

- **OpenAPI Documentation** – Auto-generated API docs with Swagger and Redoc.
- **Book Management** – Fetch books externally and manage locally stored books.
- **Discussion Threads** – Users can create chat rooms and comment on books.
- **Database Support** – Uses an ORM to persist books, users, and discussions.

## Tech Stack

- **FastAPI** – High-performance web framework for APIs.
- **PostgreSQL** – Stores books and chat threads.
- **SQLAlchemy/Pydantic** – Data modeling and validation.
- **Alembic** – Database migrations for SQLAlchemy models.
- **Poetry** – Dependency management.
- **Docker & Docker Compose** – Containerization and orchestration for deployment.
- **MyPy** – Static type checking for Python code.

## Setup

### Install Poetry

Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed before proceeding.  

You can install Poetry using the official installer:  

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### Install Dependencies

```sh
make install
```

### Run Linters

Run auto-formatting and static analysis checks:

```sh
make lint
```

### Run the Application

Start the FastAPI application:

```sh
make run
```

## Notes

This is a scaffold project that'll serve as the skeletal framework for another project. It does not include authentication, and chat rooms and messages cannot be updated or deleted.
