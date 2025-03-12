# Django REST API Learning Project

This repository serves as a comprehensive guide and practical example for learning Django REST Framework and REST API development, including CRUD operations and testing with Postman.

## Table of Contents
1. [Introduction](#introduction)
2. [Technologies](#technologies)
3. [Project Setup](#project-setup)
4. [Django Basics](#django-basics)
5. [REST API Concepts](#rest-api-concepts)
6. [Django REST Framework](#django-rest-framework)
7. [CRUD Operations](#crud-operations)
8. [Testing with Postman](#testing-with-postman)
9. [Common Commands](#common-commands)

## Introduction

This project is a Task Management API that demonstrates how to build REST APIs using Django and Django REST Framework. It includes examples of CRUD operations, API documentation, and testing guidelines.

## Technologies

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django REST Framework (DRF)**: A powerful toolkit for building Web APIs in Django.
- **PostgreSQL**: An open-source relational database system.
- **Postman**: A platform for API development and testing.

## Project Setup

### 1. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Create Django project:

```bash
django-admin startproject taskmanager .
```

### 4. Create an app:

```bash
python manage.py startapp tasks
```

### 5. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser:

```bash
python manage.py createsuperuser
```

### 7. Run the server:

```bash
python manage.py runserver
```

## Django Basics

Django follows the Model-View-Template (MVT) architecture:

### 1. Models

Models define your database schema. Example:

```python
# tasks/models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

### 2. Views

Views handle the business logic of your application. In Django, views decide what data to display.

### 3. Templates

Templates define how the data is presented to users (HTML).

### 4. URLs

URLs map URL patterns to views.

## REST API Concepts

REST (Representational State Transfer) is an architectural style for building web services:

1. **Resources**: Everything is a resource that can be accessed via a unique URI.
2. **HTTP Methods**: Use standard HTTP methods (GET, POST, PUT, DELETE).
3. **Stateless**: Each request contains all information needed to complete it.
4. **Representation**: Resources can have multiple representations (JSON, XML).

### HTTP Methods in REST:

- **GET**: Retrieve data
- **POST**: Create new data
- **PUT/PATCH**: Update existing data
- **DELETE**: Remove data

## Django REST Framework

Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django:

### Key Components:

1. **Serializers**: Convert model instances to JSON (and back).
2. **ViewSets**: Combine CRUD operations in a single class.
3. **Routers**: Automatically generate URL patterns.
4. **Authentication**: Built-in support for various authentication methods.
5. **Permissions**: Control access to API endpoints.

## CRUD Operations

CRUD stands for Create, Read, Update, and Delete, which are the four basic operations for persistent storage:

### In Django REST Framework:

1. **Create**: POST method to add new resources.
2. **Read**: GET method to retrieve resources.
3. **Update**: PUT/PATCH methods to modify existing resources.
4. **Delete**: DELETE method to remove resources.

## Testing with Postman

Postman is a popular API client that makes it easy to test API endpoints:

### Steps to Test APIs with Postman:

1. **Create a Collection**: Organize your API requests.
2. **Set Up Environments**: For different settings (dev, prod).
3. **Send Requests**: Test your API endpoints with different HTTP methods.
4. **Write Tests**: Validate responses using Postman's testing features.
5. **Use Variables**: Store and reuse values like tokens and IDs.

### Example Requests for Task API:

- **GET /api/tasks/**: List all tasks
- **POST /api/tasks/**: Create a new task
- **GET /api/tasks/{id}/**: Retrieve a specific task
- **PUT/PATCH /api/tasks/{id}/**: Update a task
- **DELETE /api/tasks/{id}/**: Delete a task

## Common Commands

```bash
# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Shell
python manage.py shell
```

---

This README serves as a guide for learning Django REST API development. The project structure and code examples provide practical implementations of the concepts discussed. 