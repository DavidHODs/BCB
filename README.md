# FastAPI Learning Project – Book Club API

This project is a structured learning exercise to explore **FastAPI** while reinforcing backend and DevOps principles. As a backend + devops engineer, the goal is to understand FastAPI’s architecture, request handling, async capabilities, and its comparison to other backend frameworks.

## Overview

This API simulates a **Book Club** where users can:

- Search for books summary locally and externally via Gutendex API.
- Review and rate books.
- Engage in discussion threads related to books.

## Features

- **OpenAPI Documentation** – Auto-generated API docs with Swagger and Redoc.
- **Authentication** – Secure user management.
- **Book Management** – Fetch books externally and manage locally reviewed books.
- **User Reviews** – Track ratings and reviews per book.
- **Discussion Threads** – Users can create threads and comment on books.
- **Database Support** – Uses an ORM to persist books, users, and discussions.

## Tech Stack

- **FastAPI** – High-performance web framework for APIs.
- **PostgreSQL** – Stores books, users, reviews, and threads.
- **SQLAlchemy/Pydantic** – Data modeling and validation.
- **Poetry** – Dependency management.
- **Docker** – Containerization for deployment.
- **Nginx** – Reverse proxy.
- **Uvicorn** – Production ASGI server.

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

This project is not a tutorial but a **hands-on exploration** of FastAPI and backend engineering. It also serves as a way to integrate DevOps practices for deployment, monitoring, and scaling.
