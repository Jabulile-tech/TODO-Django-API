# Django REST Framework TODO API - Project Setup

## Project Overview

A production-ready TODO List REST API built with Django REST Framework, featuring comprehensive logging, Docker containerization, and full test coverage.

## Technology Stack

- Django 4.2+
- Django REST Framework
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development without Docker)

### Local Setup with Docker

1. Clone/download the project
2. Run: `docker-compose up --build`
3. API available at `http://localhost:8000/api/todos/`

### Local Setup without Docker

1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

### Running Tests

`docker-compose run web python manage.py test`

Or locally:
`python manage.py test`

## API Endpoints

- `POST /api/todos/` - Create a new TODO
- `GET /api/todos/` - List all TODOs
- `GET /api/todos/<id>/` - Retrieve a single TODO
- `PUT /api/todos/<id>/` - Update a TODO (full update)
- `PATCH /api/todos/<id>/` - Partial update a TODO
- `DELETE /api/todos/<id>/` - Delete a TODO

## Project Structure

- `todo_api/` - Django project settings
- `todos/` - Main app with models, views, serializers
- `todos/models.py` - Todo model definition
- `todos/serializers.py` - Request/response serializers
- `todos/views.py` - API views
- `todos/urls.py` - URL routing
- `todos/tests.py` - Unit tests
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Multi-container orchestration
- `requirements.txt` - Python dependencies
- `manage.py` - Django CLI

## Development Notes

- Logging is configured to track API actions and errors
- Proper separation of concerns between models, serializers, and views
- Comprehensive test coverage for CRUD operations
- Docker setup includes database initialization
