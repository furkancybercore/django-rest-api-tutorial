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
| GET         | `/api/tasks/unassigned_tasks/`| List all unassigned tasks          |
| POST        | `/api/tasks/{id}/assign_person/`| Assign a task to a person        |
| POST        | `/api/tasks/{id}/unassign_person/`| Unassign a task from a person  |

### Person Endpoints

| HTTP Method | Endpoint                     | Description                         |
|-------------|------------------------------|-------------------------------------|
| GET         | `/api/persons/`              | List all persons (paginated)        |
| POST        | `/api/persons/`              | Create a new person                 |
| GET         | `/api/persons/{id}/`         | Retrieve a specific person          |
| PUT         | `/api/persons/{id}/`         | Update a specific person            |
| PATCH       | `/api/persons/{id}/`         | Partially update a specific person  |
| DELETE      | `/api/persons/{id}/`         | Delete a specific person            |
| GET         | `/api/persons/{id}/tasks/`   | List all tasks assigned to a person |
| POST        | `/api/persons/{id}/assign_task/`| Assign a task to a person        |
| POST        | `/api/persons/{id}/unassign_task/`| Unassign a task from a person  |
| PUT         | `/api/persons/{id}/profile_update/`| Update a person's profile with validation |
| PATCH       | `/api/persons/{id}/profile_update/`| Partially update a person's profile with validation |

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
| assigned_to  | ForeignKey      | Reference to Person assigned to the task (optional) |
| created_at   | DateTime        | When the task was created                    |
| updated_at   | DateTime        | When the task was last updated               |

## Person Model

The Person model has the following fields:

| Field        | Type            | Description                                  |
|--------------|-----------------|----------------------------------------------|
| id           | Integer         | Primary key                                  |
| name         | String          | Person's full name                           |
| email        | String          | Person's email address                       |
| phone        | String          | Person's phone number                        |
| department   | String          | Person's department                          |
| created_at   | DateTime        | When the person was created                  |
| updated_at   | DateTime        | When the person was last updated             |

## Filtering, Searching, and Ordering

### Task Filtering

The API supports the following query parameters for the task list endpoint:

| Parameter   | Description                                          | Example                                |
|-------------|------------------------------------------------------|----------------------------------------|
| status      | Filter tasks by status                               | `/api/tasks/?status=completed`         |
| priority    | Filter tasks by priority                             | `/api/tasks/?priority=1`               |
| completed   | Filter tasks by completion status                    | `/api/tasks/?completed=true`           |
| assigned_to | Filter tasks by assigned person                      | `/api/tasks/?assigned_to=1`            |
| search      | Search in title and description                      | `/api/tasks/?search=django`            |
| ordering    | Order tasks by specified fields                      | `/api/tasks/?ordering=priority`        |

Use a minus sign to reverse the ordering: `/api/tasks/?ordering=-priority`

### Person Filtering

The API supports the following query parameters for the person list endpoint:

| Parameter   | Description                                          | Example                                |
|-------------|------------------------------------------------------|----------------------------------------|
| department  | Filter persons by department                         | `/api/persons/?department=Engineering` |
| search      | Search in name, email, and department                | `/api/persons/?search=john`            |
| ordering    | Order persons by specified fields                    | `/api/persons/?ordering=name`          |

Use a minus sign to reverse the ordering: `/api/persons/?ordering=-created_at`

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

### Creating a Person (JSON)

```json
POST /api/persons/
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "department": "Engineering"
}
```

### Updating a Person's Profile (JSON)

```json
PUT /api/persons/1/profile_update/
{
    "name": "John Doe Updated",
    "email": "john.updated@example.com",
    "confirm_email": "john.updated@example.com",
    "phone": "+1234567890",
    "department": "Software Development"
}
```

The profile update endpoint includes special validations:
- Email format validation
- Email uniqueness validation
- Email confirmation (optional)
- Name length validation (minimum 2 characters)
- Authentication required

You can also use PATCH for partial updates:

```json
PATCH /api/persons/1/profile_update/
{
    "department": "Research & Development"
}
```

### Assigning a Task to a Person (JSON)

```json
POST /api/tasks/1/assign_person/
{
    "person_id": 1
}
```

OR

```json
POST /api/persons/1/assign_task/
{
    "task_id": 1
}
```

## Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Postman Guide](POSTMAN_GUIDE.md) - Guide for testing the API with Postman
- [User Guide](USER_GUIDE.md) - Step-by-step instructions on using and extending the API