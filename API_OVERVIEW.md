# Task Manager API Overview

This document provides an overview of the Task Manager API endpoints and functionality.

## API Endpoints

All API endpoints are prefixed with `/api/`.

### Task Endpoints

| HTTP Method | Endpoint                     | Description                         |
|-------------|------------------------------|-------------------------------------|
| GET         | `/api/tasks/`                | List all tasks (paginated)          |
| POST        | `/api/tasks/`                | Create a new task                   |
| GET         | `/api/tasks/{id}/`           | Retrieve a specific task            |
| PUT         | `/api/tasks/{id}/`           | Update a specific task              |
| PATCH       | `/api/tasks/{id}/`           | Partially update a specific task    |
| DELETE      | `/api/tasks/{id}/`           | Delete a specific task              |
| GET         | `/api/tasks/completed_tasks/`| List all completed tasks            |
| GET         | `/api/tasks/pending_tasks/`  | List all pending tasks              |

### Authentication Endpoints

| HTTP Method | Endpoint              | Description                          |
|-------------|------------------------|--------------------------------------|
| GET         | `/api-auth/login/`    | Login to the API                     |
| GET         | `/api-auth/logout/`   | Logout from the API                  |

### Documentation Endpoints

| HTTP Method | Endpoint        | Description                                    |
|-------------|-----------------|------------------------------------------------|
| GET         | `/swagger/`     | API documentation with Swagger UI              |
| GET         | `/redoc/`       | API documentation with ReDoc                   |

## Task Model

The Task model has the following fields:

| Field        | Type            | Description                                  |
|--------------|-----------------|----------------------------------------------|
| id           | Integer         | Primary key                                  |
| title        | String          | Task title                                   |
| description  | Text            | Task description (optional)                  |
| status       | String          | Task status (choices: pending, in_progress, completed, cancelled) |
| priority     | Integer         | Task priority                                |
| due_date     | Date            | Task due date (optional)                     |
| completed    | Boolean         | Whether the task is completed                |
| created_at   | DateTime        | When the task was created                    |
| updated_at   | DateTime        | When the task was last updated               |

## Filtering, Searching, and Ordering

The API supports the following query parameters for the task list endpoint:

| Parameter   | Description                                          | Example                                |
|-------------|------------------------------------------------------|----------------------------------------|
| status      | Filter tasks by status                               | `/api/tasks/?status=completed`         |
| priority    | Filter tasks by priority                             | `/api/tasks/?priority=1`               |
| completed   | Filter tasks by completion status                    | `/api/tasks/?completed=true`           |
| search      | Search in title and description                      | `/api/tasks/?search=django`            |
| ordering    | Order tasks by specified fields                      | `/api/tasks/?ordering=priority`        |

Use a minus sign to reverse the ordering: `/api/tasks/?ordering=-priority`

## API Authentication

The API uses Django's built-in authentication system. To access protected endpoints:

1. Log in through the browsable API at `/api-auth/login/`
2. Use basic authentication in your API client

## Examples

### Creating a Task (JSON)

```json
POST /api/tasks/
{
    "title": "Learn Django",
    "description": "Complete Django tutorial",
    "status": "pending",
    "priority": 1,
    "due_date": "2023-04-01"
}
```

### Updating a Task Status (JSON)

```json
PATCH /api/tasks/1/
{
    "status": "completed",
    "completed": true
}
```

## Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Postman Guide](POSTMAN_GUIDE.md) - Guide for testing the API with Postman 