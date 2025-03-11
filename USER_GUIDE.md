# User Guide: Django REST API Task Manager

This guide explains how to use the Task Manager API with step-by-step instructions and clear examples. It's designed for beginners who want to understand both the functionality and the underlying code.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Running the Application](#running-the-application)
3. [Basic Use Cases](#basic-use-cases)
4. [Advanced Use Cases](#advanced-use-cases)
5. [Understanding the Code Flow](#understanding-the-code-flow)
6. [Extending the Application](#extending-the-application)
7. [Troubleshooting](#troubleshooting)

## Getting Started

Before you begin, make sure you have:
- Python 3.8 or higher installed
- Git installed (to clone the repository)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/furkancybercore/django-rest-api-tutorial.git
   cd django-rest-api-tutorial
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data** (optional):
   ```bash
   python manage.py shell < create_sample_data.py
   ```

## Running the Application

To start the development server:

```bash
python manage.py runserver
```

This will start the server at http://127.0.0.1:8000/

**Important URLs**:
- API Endpoints: http://127.0.0.1:8000/api/tasks/
- Admin Interface: http://127.0.0.1:8000/admin/
- API Documentation (Swagger): http://127.0.0.1:8000/swagger/
- API Documentation (ReDoc): http://127.0.0.1:8000/redoc/

## Basic Use Cases

### 1. Viewing All Tasks

To view all tasks, you can:
- Visit http://127.0.0.1:8000/api/tasks/ in your browser
- Send a GET request to this endpoint using Postman

**How the code handles this**:
1. The URL `/api/tasks/` maps to the `list` action in `TaskViewSet`
2. Django REST Framework calls `get_queryset()` to retrieve all tasks
3. The `get_serializer_class()` method selects `TaskListSerializer` for list views
4. The tasks are serialized to JSON and returned with pagination

### 2. Creating a New Task

To create a new task:
- Send a POST request to http://127.0.0.1:8000/api/tasks/ with JSON data
- Use the Django admin at http://127.0.0.1:8000/admin/tasks/task/add/

**Example JSON for creating a task**:
```json
{
    "title": "Learn Django",
    "description": "Complete the Django REST framework tutorial",
    "status": "pending",
    "priority": 1,
    "due_date": "2023-04-15"
}
```

**Required fields**:
- `title`: The task title (string)

**Optional fields**:
- `description`: Task details (text)
- `status`: One of "pending", "in_progress", "completed", or "cancelled" (defaults to "pending")
- `priority`: Integer (defaults to 0)
- `due_date`: Date in YYYY-MM-DD format (can be null)
- `completed`: Boolean (defaults to false)

**How the code handles this**:
1. The URL `/api/tasks/` with POST method maps to the `create` action in `TaskViewSet`
2. Django REST Framework uses `TaskSerializer` to validate and convert the JSON data
3. If valid, a new Task instance is created in the database
4. The created task is serialized and returned with a 201 Created status

### 3. Viewing a Specific Task

To view details of a specific task:
- Visit http://127.0.0.1:8000/api/tasks/1/ (replace "1" with the task ID)
- Send a GET request to this endpoint using Postman

**How the code handles this**:
1. The URL `/api/tasks/{id}/` maps to the `retrieve` action in `TaskViewSet`
2. Django REST Framework fetches the task with the specified ID
3. The task is serialized using `TaskSerializer` (full details)
4. The serialized task is returned as JSON

### 4. Updating a Task

To update a task:
- Send a PUT request (full update) to http://127.0.0.1:8000/api/tasks/1/
- Send a PATCH request (partial update) to http://127.0.0.1:8000/api/tasks/1/

**Example JSON for updating a task status**:
```json
{
    "status": "completed",
    "completed": true
}
```

**How the code handles this**:
1. The URL `/api/tasks/{id}/` with PUT/PATCH maps to `update`/`partial_update` in `TaskViewSet`
2. Django REST Framework uses `TaskSerializer` to validate the data
3. The task is updated in the database
4. The updated task is serialized and returned

### 5. Deleting a Task

To delete a task:
- Send a DELETE request to http://127.0.0.1:8000/api/tasks/1/

**How the code handles this**:
1. The URL `/api/tasks/{id}/` with DELETE maps to the `destroy` action in `TaskViewSet`
2. Django REST Framework deletes the task from the database
3. A 204 No Content response is returned

## Advanced Use Cases

### 1. Filtering Tasks

You can filter tasks using query parameters:

- By status: http://127.0.0.1:8000/api/tasks/?status=completed
- By priority: http://127.0.0.1:8000/api/tasks/?priority=1
- By completion: http://127.0.0.1:8000/api/tasks/?completed=true

**How the code handles this**:
1. The `filter_backends` in `TaskViewSet` includes `DjangoFilterBackend`
2. The `filterset_fields` specify which fields can be used for filtering
3. Django REST Framework applies the filters to the queryset

### 2. Searching Tasks

You can search tasks by title or description:

http://127.0.0.1:8000/api/tasks/?search=django

**How the code handles this**:
1. The `filter_backends` in `TaskViewSet` includes `SearchFilter`
2. The `search_fields` specify which fields are searched
3. Django REST Framework performs a case-insensitive search across these fields

### 3. Ordering Tasks

You can order tasks by various fields:

- By priority: http://127.0.0.1:8000/api/tasks/?ordering=priority
- By due date (descending): http://127.0.0.1:8000/api/tasks/?ordering=-due_date
- By multiple fields: http://127.0.0.1:8000/api/tasks/?ordering=priority,created_at

**How the code handles this**:
1. The `filter_backends` in `TaskViewSet` includes `OrderingFilter`
2. The `ordering_fields` specify which fields can be used for ordering
3. Django REST Framework applies the ordering to the queryset

### 4. Custom Endpoints

The API includes custom endpoints for specific use cases:

- List completed tasks: http://127.0.0.1:8000/api/tasks/completed_tasks/
- List pending tasks: http://127.0.0.1:8000/api/tasks/pending_tasks/

**How the code handles this**:
1. These endpoints are defined using the `@action` decorator in `TaskViewSet`
2. Each action method applies specific filters to the queryset
3. The filtered queryset is serialized and returned

## Understanding the Code Flow

When you make an API request, here's what happens behind the scenes:

1. **URL Routing**:
   - Django receives the HTTP request and uses `urlpatterns` to determine which view should handle it
   - For API requests, the router directs them to the appropriate `TaskViewSet` method

2. **ViewSet Processing**:
   - The ViewSet determines the action to take based on the HTTP method and URL
   - It retrieves and filters data from the database using the model
   - It applies permissions and authentication checks (if configured)

3. **Serialization**:
   - The ViewSet uses serializers to convert model instances to JSON (for responses)
   - Or deserializes JSON to model instances (for requests)
   - Serializers also handle validation

4. **Response**:
   - Django REST Framework generates an HTTP response with the appropriate status code
   - The response includes the serialized data (if applicable)

## Extending the Application

### Adding a New Field to Task Model

To add a new field (e.g., "tags"):

1. **Update the model** in `tasks/models.py`:
   ```python
   class Task(models.Model):
       # Existing fields...
       tags = models.CharField(max_length=100, blank=True)
   ```

2. **Create and apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. The field will automatically be included in `TaskSerializer` (since it uses `fields = '__all__'`)

### Adding a New Endpoint

To add a new custom endpoint (e.g., high priority tasks):

1. **Add a new action** to `TaskViewSet` in `tasks/views.py`:
   ```python
   @action(detail=False, methods=['get'])
   def high_priority(self, request):
       """List all high priority tasks (priority <= 2)."""
       high_priority_tasks = Task.objects.filter(priority__lte=2)
       serializer = self.get_serializer(high_priority_tasks, many=True)
       return Response(serializer.data)
   ```

2. The endpoint will automatically be available at `/api/tasks/high_priority/`

### Adding Related Models

To add a new model related to Task (e.g., "Project"):

1. **Create the new model** in `tasks/models.py`:
   ```python
   class Project(models.Model):
       name = models.CharField(max_length=100)
       description = models.TextField(blank=True)
       
       def __str__(self):
           return self.name
   
   class Task(models.Model):
       # Add foreign key to existing Task model
       project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE, null=True)
       # Existing fields...
   ```

2. **Create a serializer** in `tasks/serializers.py`:
   ```python
   class ProjectSerializer(serializers.ModelSerializer):
       class Meta:
           model = Project
           fields = '__all__'
   ```

3. **Create a ViewSet** in `tasks/views.py`:
   ```python
   class ProjectViewSet(viewsets.ModelViewSet):
       queryset = Project.objects.all()
       serializer_class = ProjectSerializer
   ```

4. **Register in the router** in `tasks/urls.py`:
   ```python
   router.register(r'projects', ProjectViewSet)
   ```

5. **Create and apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Troubleshooting

### Common Issues

1. **"Error: connect ECONNREFUSED 127.0.0.1:8000"**:
   - The development server is not running. Start it with `python manage.py runserver`
   - Ensure the server is running on the expected port (default is 8000)

2. **"Module not found" errors**:
   - Make sure the virtual environment is activated
   - Check that all dependencies are installed with `pip install -r requirements.txt`

3. **Database errors**:
   - Ensure migrations are applied with `python manage.py migrate`
   - Check database settings in `settings.py`

4. **Serializer validation errors**:
   - Check the format of your JSON data
   - Ensure all required fields are provided
   - Verify that field values meet the model constraints (e.g., length, choices) 