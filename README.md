# Django REST Framework TODO API

A production-ready TODO List REST API built with Django REST Framework, featuring comprehensive logging, Docker containerization, PostgreSQL support, and full test coverage.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Logging](#logging)
- [Development Notes](#development-notes)

## ✨ Features

- ✅ **Complete CRUD Operations** - Create, Read, Update, and Delete TODO items
- 📊 **Comprehensive Logging** - Track API actions and errors with detailed logging
- 🐳 **Docker Support** - Full containerization with Docker and Docker Compose
- 📚 **REST API** - Clean, RESTful API using Django REST Framework
- ✔️ **Input Validation** - Request validation with DRF serializers
- 🧪 **Full Test Coverage** - Comprehensive unit tests for all CRUD operations
- 📝 **API Documentation** - Clear API endpoint documentation
- 🏗️ **Clean Architecture** - Strict separation of concerns (models, serializers, views, urls)
- ⚡ **Pagination** - Built-in pagination support
- 🔍 **Search & Filtering** - Search and filter capabilities for TODO items

## 🛠️ Technology Stack

- **Python 3.11+**
- **Django 4.2+**
- **Django REST Framework 3.14+**
- **PostgreSQL 15** (optional, SQLite for local development)
- **Docker & Docker Compose**
- **Gunicorn** (production WSGI server)

## 📁 Project Structure

```
.
├── .github/
│   └── copilot-instructions.md
├── todo_api/                    # Main Django project
│   ├── __init__.py
│   ├── settings.py              # Django settings with logging config
│   ├── urls.py                  # Main URL routing
│   ├── asgi.py                  # ASGI config
│   └── wsgi.py                  # WSGI config
├── todos/                       # Main API app
│   ├── migrations/              # Database migrations
│   ├── __init__.py
│   ├── apps.py                  # App configuration
│   ├── models.py                # Todo model definition
│   ├── serializers.py           # DRF serializers with validation
│   ├── views.py                 # API views with CRUD operations
│   ├── urls.py                  # App URL routing
│   └── tests.py                 # Comprehensive test suite
├── manage.py                    # Django management CLI
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker container configuration
├── docker-compose.yml           # Multi-container orchestration
├── .gitignore                   # Git ignore rules
├── .dockerignore                # Docker ignore rules
└── README.md                    # This file
```

## 🚀 Installation & Setup

### Prerequisites

- **Docker & Docker Compose** (for containerized setup)
- **Python 3.11+** (for local development)
- **pip** (Python package manager)

### Option 1: Quick Start with Docker (Recommended)

1. **Clone/Download the project**

   ```bash
   cd "Tati Software Technical Assessment"
   ```

2. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

3. **Access the API**
   - API will be available at: `http://localhost:8000/api/todos/`
   - Admin panel at: `http://localhost:8000/admin/`

4. **Create a superuser (optional, for admin access)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### Option 2: Local Setup without Docker

1. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   - API will be available at: `http://localhost:8000/api/todos/`
   - Admin panel at: `http://localhost:8000/admin/`

## 🎯 Running the Application

### Using Docker Compose

**Start the application:**

```bash
docker-compose up
```

**Stop the application:**

```bash
docker-compose down
```

**View logs:**

```bash
docker-compose logs -f web
```

**Run a specific command:**

```bash
docker-compose exec web python manage.py [command]
```

### Running Locally

**Start the development server:**

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/todos/`

## 📡 API Endpoints

All endpoints are prefixed with `/api/` and return JSON responses.

### Todo Endpoints

#### Create a new TODO

```http
POST /api/todos/
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false
}
```

**Response (201 Created):**

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "created_at": "2024-05-27T10:30:00Z",
  "updated_at": "2024-05-27T10:30:00Z"
}
```

---

#### List all TODOs

```http
GET /api/todos/
```

**Response (200 OK):**

```json
{
  "count": 10,
  "next": "http://localhost:8000/api/todos/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "is_completed": false,
      "created_at": "2024-05-27T10:30:00Z",
      "updated_at": "2024-05-27T10:30:00Z"
    }
  ]
}
```

---

#### Retrieve a single TODO

```http
GET /api/todos/{id}/
```

**Response (200 OK):**

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "created_at": "2024-05-27T10:30:00Z",
  "updated_at": "2024-05-27T10:30:00Z"
}
```

**Response (404 Not Found):**

```json
{
  "detail": "Todo not found"
}
```

---

#### Full update a TODO (PUT)

```http
PUT /api/todos/{id}/
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description",
  "is_completed": true
}
```

**Response (200 OK):** Returns updated todo object

---

#### Partial update a TODO (PATCH)

```http
PATCH /api/todos/{id}/
Content-Type: application/json

{
  "is_completed": true
}
```

**Response (200 OK):** Returns updated todo object

---

#### Delete a TODO

```http
DELETE /api/todos/{id}/
```

**Response (204 No Content):** Empty response, todo is deleted

---

#### Get completed TODOs

```http
GET /api/todos/completed/
```

**Response (200 OK):** List of only completed todos

---

#### Get pending TODOs

```http
GET /api/todos/pending/
```

**Response (200 OK):** List of only incomplete todos

### Error Responses

**Invalid request (400 Bad Request):**

```json
{
  "title": ["Title cannot be empty."]
}
```

**Not found (404 Not Found):**

```json
{
  "detail": "Todo not found"
}
```

## 🧪 Running Tests

### Using Docker Compose

Run all tests:

```bash
docker-compose run web python manage.py test
```

Run tests for specific module:

```bash
docker-compose run web python manage.py test todos.tests.TodoModelTest
```

Run tests with verbosity:

```bash
docker-compose run web python manage.py test -v 2
```

### Running Tests Locally

Run all tests:

```bash
python manage.py test
```

Run tests for specific module:

```bash
python manage.py test todos.tests.TodoModelTest
```

Run tests with coverage:

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Coverage

The test suite includes:

1. **Model Tests**
   - Todo creation
   - String representation
   - Default values
   - Optional fields
   - Timestamp handling

2. **API Tests**
   - Create TODO (valid & invalid)
   - List all TODOs
   - Retrieve single TODO
   - Full and partial updates
   - Delete TODO
   - Custom endpoints (completed, pending)
   - Error handling (404, 400)
   - Validation errors

3. **Serializer Tests**
   - Valid data validation
   - Empty title handling
   - Whitespace handling
   - Field validation

## 📊 Logging

The application implements comprehensive logging configured in `todo_api/settings.py`.

### Log Files

Logs are stored in the `logs/` directory:

- **`logs/django.log`** - General Django logs
- **`logs/todos.log`** - TODO app specific logs
- **`logs/errors.log`** - Error logs only

### Log Configuration

The logging system tracks:

- **API Actions:**
  - Todo creation with request data
  - Todo retrieval and listing
  - Todo updates (full and partial)
  - Todo deletion

- **Error Handling:**
  - Validation errors
  - Not found errors (404)
  - Request failures

- **Debug Information:**
  - View execution
  - Data access patterns
  - Serializer operations

### Log Format

Logs include:

- Timestamp
- Log level (DEBUG, INFO, WARNING, ERROR)
- Module name
- Process ID and Thread ID
- Message content

**Example log entry:**

```
INFO 2024-05-27 10:30:15,123 todos.views 12345 45678 Creating new todo with data: {'title': 'Buy groceries', 'description': 'Milk, eggs, bread'}
INFO 2024-05-27 10:30:15,456 todos.views 12345 45678 Successfully created todo with ID: 1
```

## 💡 Development Notes

### Architecture Principles

1. **Separation of Concerns**
   - **Models** (`models.py`) - Define database schema
   - **Serializers** (`serializers.py`) - Handle validation and data transformation
   - **Views** (`views.py`) - Implement business logic and API operations
   - **URLs** (`urls.py`) - Route requests to views
   - **Tests** (`tests.py`) - Ensure code quality and functionality

2. **Input Validation**
   - All inputs validated using DRF serializers
   - Title is required and non-empty
   - Description is optional
   - Automatic validation error responses

3. **Error Handling**
   - Proper HTTP status codes (201, 200, 400, 404, 204)
   - Descriptive error messages
   - Comprehensive error logging

4. **Database Optimization**
   - Indexed fields (created_at, is_completed)
   - Automatic ordering by creation date
   - Efficient query patterns

### Adding New Features

To add new endpoints:

1. Create a new method in `TodoViewSet` in `views.py`
2. Use `@action` decorator for custom actions
3. Add corresponding tests in `tests.py`
4. Update logging as needed
5. Add documentation to this README

### Configuration

Key configuration in `todo_api/settings.py`:

- **DEBUG** - Set to `False` in production
- **ALLOWED_HOSTS** - Configure for production domains
- **DATABASES** - Switch to PostgreSQL for production
- **LOGGING** - Adjust log levels as needed
- **REST_FRAMEWORK** - Customize API behavior

## 📝 Postman Collection

To import the API collection in Postman:

1. Open Postman
2. Click **Import** button
3. Select the collection file from the project folder
4. Collection will be imported with all endpoints
5. Set the base URL to `http://localhost:8000/api/`
6. Execute requests directly

## 🔒 Security Notes

For production deployment:

- [ ] Change `SECRET_KEY` in settings
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use environment variables for sensitive data
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS if needed
- [ ] Use a production database (PostgreSQL)
- [ ] Implement authentication and permissions
- [ ] Use a robust secret key
- [ ] Enable CSRF protection

## 📞 Support & Troubleshooting

### Common Issues

**Port already in use:**

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

**Database migration errors:**

```bash
# Reset migrations (development only)
python manage.py migrate todos zero
python manage.py migrate
```

**Docker build failures:**

```bash
# Clean rebuild
docker-compose down
docker-compose up --build --force-recreate
```

## 📄 License

This project is provided for the technical assessment.

---

**Last Updated:** May 27, 2024
**Version:** 1.0.0
