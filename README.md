# Publishing Workflow API

A small REST API project built as a practical backend development exercise using FastAPI, SQLAlchemy, PostgreSQL, Docker and pytest.

## Tech stack

- Python 3.10
- FastAPI
- Pydantic
- SQLAlchemy ORM
- PostgreSQL
- Docker
- Docker Compose
- pytest

## Features

- Health check endpoint
- Create articles
- List articles
- Get article by ID
- Update articles
- Delete articles
- Request validation
- HTTP 404 handling
- PostgreSQL persistence
- Dockerized API and database
- Automated API tests
- Isolated in-memory test database

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| GET | `/articles` | List all articles |
| GET | `/articles/{id}` | Get one article |
| POST | `/articles` | Create an article |
| PATCH | `/articles/{id}` | Update an article |
| DELETE | `/articles/{id}` | Delete an article |

Interactive API documentation is available at:

`http://localhost:8000/docs`

## Running with Docker

Create a local `.env` file based on `.env.example`.

Then run:

```bash
docker compose up --build -d
```

Check containers:

```bash
docker compose ps
```

The API will be available at:

`http://localhost:8000`

## Running tests

```bash
python -m pytest -v
```

The test suite covers API health checks, CRUD operations, validation errors and 404 responses.

Tests use an isolated in-memory SQLite database instead of the development PostgreSQL database.

## Architecture

```text
Client
  |
  v
FastAPI
  |
  v
Pydantic validation
  |
  v
SQLAlchemy ORM
  |
  v
PostgreSQL
```

When running with Docker Compose:

```text
Browser
   |
   v
publishing-api container
   |
   v
Docker network
   |
   v
publishing-postgres container
   |
   v
persistent Docker volume
```

## Purpose

This project demonstrates practical experience with REST API development, ORM-based persistence, containerization, relational databases and automated testing.
