# Django REST API Learning Project

This repository serves as a comprehensive learning resource for Django REST Framework and REST API development. It includes a complete task management API with documentation and testing examples.

## 📚 Additional Documentation

- [User Guide](USER_GUIDE.md) - Step-by-step instructions on using and extending the API
- [API Overview](API_OVERVIEW.md) - Complete overview of all API endpoints and functionality
- [Postman Guide](POSTMAN_GUIDE.md) - Detailed instructions for testing the API with Postman

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Django Basics](#django-basics)
4. [Setting Up the Project](#setting-up-the-project)
5. [Creating the Task Model](#creating-the-task-model)
6. [Serializers in Django REST Framework](#serializers-in-django-rest-framework)
7. [Views and ViewSets](#views-and-viewsets)
8. [URL Routing](#url-routing)
9. [Django Admin Configuration](#django-admin-configuration)
10. [API Documentation](#api-documentation)
11. [Testing the API](#testing-the-api)
12. [Common Commands](#common-commands)

## 📖 Introduction

This project is a Task Management API that demonstrates how to build REST APIs using Django and Django REST Framework. As a beginner, you'll learn the fundamentals of building web APIs while following best practices.

### What is Django?

Django is a high-level Python web framework that follows the "batteries-included" philosophy, providing everything developers need to build web applications quickly. It follows the Model-View-Template (MVT) architecture.

### What is Django REST Framework (DRF)?

Django REST Framework is a powerful toolkit built on top of Django that makes it easy to build Web APIs. It includes features like serialization, authentication, viewsets, and browsable API interfaces.

### What is a REST API?

REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs use HTTP methods explicitly and are stateless, making them simple, scalable, and reliable.

## 🏗️ Project Structure

Here's the structure of our project:

```
django_rest_api_tutorial/
├── taskmanager/            # Main Django project folder
│   ├── __init__.py
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL routing
│   ├── asgi.py
│   └── wsgi.py
├── tasks/                  # Tasks app folder
│   ├── migrations/         # Database migrations
│   ├── __init__.py
│   ├── admin.py            # Admin interface configuration
│   ├── apps.py
│   ├── models.py           # Data models
│   ├── serializers.py      # DRF serializers
│   ├── tests.py            # API tests
│   ├── urls.py             # App URL routing
│   └── views.py            # API views and logic
├── venv/                   # Virtual environment (not in repo)
├── manage.py               # Django management script
├── requirements.txt        # Project dependencies
├── README.md               # This file
├── API_OVERVIEW.md         # API documentation
├── POSTMAN_GUIDE.md        # Guide for Postman testing
└── create_sample_data.py   # Script to create sample data
```

## 🧠 Django Basics

Django follows the Model-View-Template (MVT) architecture:

### Models

Models define your database schema. They are Python classes that inherit from `django.db.models.Model`. Each attribute in the class represents a database field.

For example, our Task model has fields like title, description, status, etc. Django automatically creates database tables based on these model definitions.

### Views

Views handle the business logic of your application. In Django, views decide what data to display and how to process user input. With Django REST Framework, we use ViewSets instead of traditional Django views, which provide a higher level of abstraction.

### Templates

Templates define how the data is presented to users. In a REST API, we don't typically use templates since we're returning JSON data instead of HTML. Instead, serializers handle converting our data to JSON.

### URLs

URLs map URL patterns to views. Django's URL dispatcher sends requests to the appropriate view based on the URL pattern. With DRF's routers, URL configuration becomes even simpler.

## 🛠️ Setting Up the Project

To set up the project from scratch, I followed these steps:

### 1. Created a Virtual Environment

Virtual environments keep project dependencies isolated:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 2. Installed Dependencies

The requirements.txt file lists all project dependencies:

```
Django==4.2.10
djangorestframework==3.14.0
markdown==3.5.1
django-filter==23.5
pygments==2.17.2
pytest==7.4.4
pytest-django==4.7.0
python-dotenv==1.0.0
psycopg2-binary==2.9.9
drf-yasg==1.21.7
pyyaml==6.0.1
uritemplate==4.1.1
```

I installed them with:

```bash
pip install -r requirements.txt
```

### 3. Created Django Project

```bash
django-admin startproject taskmanager .
```

### 4. Created Django App

```bash
python manage.py startapp tasks
```

### 5. Configured Settings

In `taskmanager/settings.py`, I added our app and third-party packages:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom apps
    'tasks',
    # Third-party apps
    'rest_framework',
    'django_filters',
    'drf_yasg',
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
```

## 📝 Creating the Task Model

The model is the foundation of our application, defining what data we'll store. I created a Task model in `tasks/models.py`:

```python
from django.db import models

class Task(models.Model):
    """
    Task model representing a task in the task management system.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.IntegerField(default=0)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority', 'due_date', 'created_at']
    
    def __str__(self):
        return self.title
```

Let's break down this model:

- **CharField**: For storing text with a limited length.
  - `max_length`: Maximum length of text.
- **TextField**: For longer text without length limit.
  - `blank=True`: Field is optional.
- **IntegerField**: For storing integers.
- **DateField**: For storing dates.
  - `null=True`: Field can be NULL in the database.
- **BooleanField**: For storing True/False values.
- **DateTimeField**: For storing date and time.
  - `auto_now_add=True`: Automatically set to current time when created.
  - `auto_now=True`: Automatically updated on save.
- **STATUS_CHOICES**: Tuple of (value, display_name) pairs for dropdown options.
- **Meta class**: Contains metadata about the model.
  - `ordering`: Default order for queries.
- **__str__**: String representation of the object.

After creating the model, I ran these commands to create and apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🔄 Serializers in Django REST Framework

Serializers convert Django model instances to JSON and vice versa. They're how our API speaks to the outside world.

In `tasks/serializers.py`, I created two serializers:

```python
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    This is used to convert Task instances to JSON and vice versa.
    """
    class Meta:
        model = Task
        fields = '__all__'  # Serializes all fields
        read_only_fields = ('created_at', 'updated_at')  # These fields are read-only


class TaskListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing tasks.
    Shows fewer fields than the complete serializer.
    """
    class Meta:
        model = Task
        fields = ('id', 'title', 'status', 'priority', 'due_date', 'completed')
```

Serializer key concepts:

- **ModelSerializer**: A class that automatically creates serializers based on your model.
- **Meta class**: Configuration for the serializer.
  - `model`: The model to serialize.
  - `fields`: Which fields to include.
  - `read_only_fields`: Fields that can't be modified via the API.
- **Multiple serializers**: I created two serializers for different purposes.
  - `TaskSerializer`: Complete serializer for detail views.
  - `TaskListSerializer`: Simplified serializer for list views.

## 👁️ Views and ViewSets

Views handle API requests and responses. In Django REST Framework, ViewSets combine multiple related views into a single class.

In `tasks/views.py`, I created a TaskViewSet:

```python
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer, TaskListSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Task instances.
    
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'completed']
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'due_date', 'created_at']
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions:
        - list: Use a simplified serializer
        - other actions: Use the full serializer
        """
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer
    
    @action(detail=False, methods=['get'])
    def completed_tasks(self, request):
        """
        Custom action to list all completed tasks.
        
        URL: /api/tasks/completed_tasks/
        """
        completed_tasks = Task.objects.filter(completed=True)
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_tasks(self, request):
        """
        Custom action to list all pending tasks.
        
        URL: /api/tasks/pending_tasks/
        """
        pending_tasks = Task.objects.filter(completed=False)
        serializer = self.get_serializer(pending_tasks, many=True)
        return Response(serializer.data)
```

ViewSet key concepts:

- **ModelViewSet**: Provides default implementations for CRUD operations:
  - `list`: Get all tasks
  - `create`: Create a new task
  - `retrieve`: Get a specific task
  - `update`: Update a task
  - `destroy`: Delete a task
- **queryset**: The base queryset for the viewset.
- **serializer_class**: Which serializer to use.
- **filter_backends**: Enables filtering, searching, and ordering.
- **get_serializer_class()**: Dynamic serializer selection based on the action.
- **@action decorator**: Creates custom endpoints beyond basic CRUD.
  - `detail=False`: The action applies to the entire collection.
  - `methods=['get']**: The HTTP method(s) this action responds to.

## 🔗 URL Routing

URL routing maps URLs to views. With Django REST Framework's routers, this becomes simpler.

In `tasks/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
```

In `taskmanager/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view for Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version='v1',
        description="API for managing tasks",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('tasks.urls')),
    
    # API authentication
    path('api-auth/', include('rest_framework.urls')),
    
    # API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

URL routing key concepts:

- **Router**: Automatically generates URL patterns for all CRUD operations.
- **register**: Associates a viewset with a URL prefix.
- **include**: Includes URL patterns from another module.
- **Schema view**: Generates interactive API documentation.

The router automatically creates these URL patterns:

- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Retrieve a specific task
- `PUT /api/tasks/{id}/` - Update a specific task
- `PATCH /api/tasks/{id}/` - Partially update a specific task
- `DELETE /api/tasks/{id}/` - Delete a specific task
- `GET /api/tasks/completed_tasks/` - List completed tasks
- `GET /api/tasks/pending_tasks/` - List pending tasks

## 📊 Django Admin Configuration

Django's admin interface provides a user-friendly way to manage your data. I customized it in `tasks/admin.py`:

```python
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface for the Task model.
    """
    list_display = ('title', 'status', 'priority', 'due_date', 'completed', 'created_at')
    list_filter = ('status', 'priority', 'completed')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Status Information', {
            'fields': ('status', 'priority', 'due_date', 'completed')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

Admin configuration key concepts:

- **@admin.register**: Registers the model with the admin site.
- **list_display**: Fields to show in the list view.
- **list_filter**: Fields to filter by in the sidebar.
- **search_fields**: Fields to search in the search box.
- **date_hierarchy**: Navigate through dates.
- **readonly_fields**: Fields that cannot be edited.
- **fieldsets**: Group fields together in the detail view.

## 📑 API Documentation

I set up automatic API documentation using drf-yasg, which provides interactive documentation:

- **Swagger UI** at `/swagger/`: Interactive documentation
- **ReDoc** at `/redoc/`: More readable documentation

Additionally, I created two detailed documentation files:

- [API Overview](API_OVERVIEW.md): Comprehensive reference of all API endpoints
- [Postman Guide](POSTMAN_GUIDE.md): Step-by-step guide for testing with Postman

## 🧪 Testing the API

I created tests for our API in `tasks/tests.py`:

```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskTests(APITestCase):
    """
    Test cases for the Task API.
    """
    def setUp(self):
        """
        Set up test data.
        """
        # Create some test tasks
        self.task1 = Task.objects.create(
            title="Test Task 1",
            description="This is a test task",
            status="pending",
            priority=1
        )
        # More test tasks...
    
    def test_get_tasks_list(self):
        """
        Test retrieving a list of tasks.
        """
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    # More test methods for create, update, delete, etc.
```

Testing key concepts:

- **APITestCase**: Provides testing utilities for REST framework.
- **setUp**: Runs before each test method to set up test data.
- **reverse**: Generates URLs by their name.
- **assertEqual**: Checks if two values are equal.

Additionally, I created a script to populate the database with sample data in `create_sample_data.py`:

```python
#!/usr/bin/env python
import datetime
from tasks.models import Task

# Delete existing tasks to avoid duplication
Task.objects.all().delete()

# Create sample tasks
tasks = [
    {
        'title': 'Learn Django Basics',
        'description': 'Understand Django models, views, templates, and URLs',
        'status': 'completed',
        'priority': 1,
        'due_date': datetime.date.today() - datetime.timedelta(days=5),
        'completed': True
    },
    # More tasks...
]

# Save tasks to database
for task_data in tasks:
    task = Task(**task_data)
    task.save()
    print(f"Created task: {task.title}")
```

Run this script with:

```bash
python manage.py shell < create_sample_data.py
```

## 📋 Common Commands

Here are the most common Django commands I used during development:

```bash
# Create migrations for model changes
python manage.py makemigrations

# Apply migrations to the database
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser

# Run the development server
python manage.py runserver

# Run tests
python manage.py test

# Open a Django shell
python manage.py shell

# Load sample data
python manage.py shell < create_sample_data.py
```

## 🤝 Contributing

Feel free to fork this repository and make your own changes. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. 