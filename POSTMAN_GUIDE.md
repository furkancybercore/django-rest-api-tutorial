# Postman Guide for Task Manager API

This guide will help you test the Task Manager API using Postman.

## Table of Contents
1. [Before You Begin](#before-you-begin)
2. [Setting Up Postman](#setting-up-postman)
3. [Creating a Collection](#creating-a-collection)
4. [Basic CRUD Operations for Tasks](#basic-crud-operations-for-tasks)
5. [Person Management](#person-management)
6. [Task Assignment](#task-assignment)
7. [Custom Actions](#custom-actions)
8. [Filtering and Searching](#filtering-and-searching)
9. [Authentication](#authentication)
10. [Troubleshooting](#troubleshooting)

## Before You Begin

Before you can test the API, you need to ensure the Django development server is running:

1. Activate your virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

3. Verify the server is running by opening http://127.0.0.1:8000/api/tasks/ in your browser. You should see the Django REST Framework browsable API.

**Important**: If you're getting "Error: connect ECONNREFUSED 127.0.0.1:8000" in Postman, it means the server is not running. Make sure to complete the steps above before testing with Postman.

## Setting Up Postman

1. Download and install Postman from [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
2. Launch Postman and create an account or sign in

## Creating a Collection

1. Click on the "Collections" tab in the sidebar
2. Click the "+" button to create a new collection
3. Name your collection "Task Manager API"
4. Save the collection

## Basic CRUD Operations for Tasks

### List All Tasks (GET)

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/tasks/`
4. Save the request as "List All Tasks"
5. Click "Send" to execute the request

**Expected Response:**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Complete Django REST tutorial",
            "status": "in_progress",
            "priority": 1,
            "due_date": "2023-03-20",
            "completed": false
        },
        {
            "id": 2,
            "title": "Practice REST API concepts",
            "status": "pending",
            "priority": 2,
            "due_date": null,
            "completed": false
        }
    ]
}
```

### Create a Task (POST)

1. Create a new request in your collection
2. Set the request method to POST
3. Set the URL to `http://127.0.0.1:8000/api/tasks/`
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data:
```json
{
    "title": "Learn Postman",
    "description": "Learn how to use Postman to test APIs",
    "status": "pending",
    "priority": 1,
    "due_date": "2023-03-25"
}
```
7. Save the request as "Create Task"
8. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 3,
    "title": "Learn Postman",
    "description": "Learn how to use Postman to test APIs",
    "status": "pending",
    "priority": 1,
    "due_date": "2023-03-25",
    "completed": false,
    "created_at": "2023-03-15T10:00:00Z",
    "updated_at": "2023-03-15T10:00:00Z"
}
```

### Retrieve a Task (GET)

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/tasks/1/` (replace 1 with the ID of a task)
4. Save the request as "Get Task Detail"
5. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 1,
    "title": "Complete Django REST tutorial",
    "description": "Complete the Django REST framework tutorial and understand the concepts",
    "status": "in_progress",
    "priority": 1,
    "due_date": "2023-03-20",
    "completed": false,
    "created_at": "2023-03-15T09:00:00Z",
    "updated_at": "2023-03-15T09:00:00Z"
}
```

### Update a Task (PUT)

1. Create a new request in your collection
2. Set the request method to PUT
3. Set the URL to `http://127.0.0.1:8000/api/tasks/1/` (replace 1 with the ID of a task)
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data:
```json
{
    "title": "Complete Django REST tutorial",
    "description": "Complete the Django REST framework tutorial and understand the concepts",
    "status": "completed",
    "priority": 1,
    "due_date": "2023-03-20",
    "completed": true
}
```
7. Save the request as "Update Task"
8. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 1,
    "title": "Complete Django REST tutorial",
    "description": "Complete the Django REST framework tutorial and understand the concepts",
    "status": "completed",
    "priority": 1,
    "due_date": "2023-03-20",
    "completed": true,
    "created_at": "2023-03-15T09:00:00Z",
    "updated_at": "2023-03-15T10:15:00Z"
}
```

### Partial Update a Task (PATCH)

1. Create a new request in your collection
2. Set the request method to PATCH
3. Set the URL to `http://127.0.0.1:8000/api/tasks/2/` (replace 2 with the ID of a task)
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data:
```json
{
    "status": "in_progress"
}
```
7. Save the request as "Partial Update Task"
8. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 2,
    "title": "Practice REST API concepts",
    "description": "",
    "status": "in_progress",
    "priority": 2,
    "due_date": null,
    "completed": false,
    "created_at": "2023-03-15T09:30:00Z",
    "updated_at": "2023-03-15T10:20:00Z"
}
```

### Delete a Task (DELETE)

1. Create a new request in your collection
2. Set the request method to DELETE
3. Set the URL to `http://127.0.0.1:8000/api/tasks/3/` (replace 3 with the ID of a task)
4. Save the request as "Delete Task"
5. Click "Send" to execute the request

**Expected Response:**
- Status code: 204 No Content
- No response body

## Person Management

### List All Persons (GET)

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/persons/`
4. Save the request as "List All Persons"
5. Click "Send" to execute the request

**Expected Response:**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "department": "Engineering",
            "created_at": "2023-03-15T09:00:00Z",
            "updated_at": "2023-03-15T09:00:00Z"
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "+0987654321",
            "department": "Marketing",
            "created_at": "2023-03-15T10:00:00Z",
            "updated_at": "2023-03-15T10:00:00Z"
        }
    ]
}
```

### Create a Person (POST)

1. Create a new request in your collection
2. Set the request method to POST
3. Set the URL to `http://127.0.0.1:8000/api/persons/`
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data:
```json
{
    "name": "Alice Johnson",
    "email": "alice.johnson@example.com",
    "phone": "+1122334455",
    "department": "Human Resources"
}
```
7. Save the request as "Create Person"
8. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 3,
    "name": "Alice Johnson",
    "email": "alice.johnson@example.com",
    "phone": "+1122334455",
    "department": "Human Resources",
    "created_at": "2023-03-15T11:00:00Z",
    "updated_at": "2023-03-15T11:00:00Z"
}
```

### Retrieve a Person (GET)

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/persons/1/` (replace 1 with the ID of a person)
4. Save the request as "Get Person Detail"
5. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "department": "Engineering",
    "created_at": "2023-03-15T09:00:00Z",
    "updated_at": "2023-03-15T09:00:00Z",
    "assigned_tasks": [
        {
            "id": 1,
            "title": "Complete Django REST tutorial",
            "status": "completed",
            "priority": 1,
            "due_date": "2023-03-20",
            "completed": true
        }
    ]
}
```

### Update a Person (PUT)

1. Create a new request in your collection
2. Set the request method to PUT
3. Set the URL to `http://127.0.0.1:8000/api/persons/1/` (replace 1 with the ID of a person)
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data:
```json
{
    "name": "John Doe",
    "email": "john.doe.updated@example.com",
    "phone": "+1234567890",
    "department": "Software Development"
}
```
7. Save the request as "Update Person"
8. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe.updated@example.com",
    "phone": "+1234567890",
    "department": "Software Development",
    "created_at": "2023-03-15T09:00:00Z",
    "updated_at": "2023-03-15T11:30:00Z"
}
```

### Partial Update a Person (PATCH)

1. Create a new request in your collection
2. Set the request method to PATCH
3. Set the URL to `http://127.0.0.1:8000/api/persons/2/` (replace 2 with the ID of a person)
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data:
```json
{
    "department": "Digital Marketing"
}
```
7. Save the request as "Partial Update Person"
8. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "+0987654321",
    "department": "Digital Marketing",
    "created_at": "2023-03-15T10:00:00Z",
    "updated_at": "2023-03-15T11:45:00Z"
}
```

### Delete a Person (DELETE)

1. Create a new request in your collection
2. Set the request method to DELETE
3. Set the URL to `http://127.0.0.1:8000/api/persons/3/` (replace 3 with the ID of a person)
4. Save the request as "Delete Person"
5. Click "Send" to execute the request

**Expected Response:**
- Status code: 204 No Content
- No response body

### Update a Person's Profile with Validation

1. Create a new request in your collection
2. Set the request method to PUT
3. Set the URL to `http://127.0.0.1:8000/api/persons/1/profile_update/` (replace 1 with the ID of a person)
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data:
```json
{
    "name": "John Doe Updated",
    "email": "john.updated@example.com",
    "confirm_email": "john.updated@example.com",
    "phone": "+1111222333",
    "department": "Software Development"
}
```
7. Go to the "Authorization" tab
8. Select "Basic Auth" from the Type dropdown
9. Enter your username and password (required for this endpoint)
10. Save the request as "Update Person Profile"
11. Click "Send" to execute the request

**Expected Response:**
```json
{
    "status": "success",
    "message": "Profile updated successfully",
    "data": {
        "name": "John Doe Updated",
        "email": "john.updated@example.com",
        "phone": "+1111222333",
        "department": "Software Development"
    }
}
```

### Partially Update a Person's Profile with Validation

1. Create a new request in your collection
2. Set the request method to PATCH
3. Set the URL to `http://127.0.0.1:8000/api/persons/1/profile_update/` (replace 1 with the ID of a person)
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data (just the fields you want to update):
```json
{
    "department": "Research & Development"
}
```
7. Go to the "Authorization" tab
8. Select "Basic Auth" from the Type dropdown
9. Enter your username and password (required for this endpoint)
10. Save the request as "Partial Update Person Profile"
11. Click "Send" to execute the request

**Expected Response:**
```json
{
    "status": "success",
    "message": "Profile updated successfully",
    "data": {
        "name": "John Doe Updated",
        "email": "john.updated@example.com",
        "phone": "+1111222333",
        "department": "Research & Development"
    }
}
```

## Task Assignment

### View Tasks Assigned to a Person

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/persons/1/tasks/` (replace 1 with the ID of a person)
4. Save the request as "View Person's Tasks"
5. Click "Send" to execute the request

**Expected Response:**
```json
[
    {
        "id": 1,
        "title": "Complete Django REST tutorial",
        "status": "completed",
        "priority": 1,
        "due_date": "2023-03-20",
        "completed": true,
        "assigned_to_name": "John Doe"
    }
]
```

### Assign a Task to a Person (from Person endpoint)

1. Create a new request in your collection
2. Set the request method to POST
3. Set the URL to `http://127.0.0.1:8000/api/persons/1/assign_task/` (replace 1 with the ID of a person)
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data:
```json
{
    "task_id": 2
}
```
7. Save the request as "Assign Task to Person"
8. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 2,
    "title": "Practice REST API concepts",
    "description": "",
    "status": "in_progress",
    "priority": 2,
    "due_date": null,
    "completed": false,
    "assigned_to": 1,
    "assigned_to_name": "John Doe",
    "created_at": "2023-03-15T09:30:00Z",
    "updated_at": "2023-03-15T12:00:00Z"
}
```

### Assign a Task to a Person (from Task endpoint)

1. Create a new request in your collection
2. Set the request method to POST
3. Set the URL to `http://127.0.0.1:8000/api/tasks/2/assign_person/` (replace 2 with the ID of a task)
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data:
```json
{
    "person_id": 2
}
```
7. Save the request as "Assign Person to Task"
8. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 2,
    "title": "Practice REST API concepts",
    "description": "",
    "status": "in_progress",
    "priority": 2,
    "due_date": null,
    "completed": false,
    "assigned_to": 2,
    "assigned_to_name": "Jane Smith",
    "created_at": "2023-03-15T09:30:00Z",
    "updated_at": "2023-03-15T12:15:00Z"
}
```

### Unassign a Task from a Person (from Person endpoint)

1. Create a new request in your collection
2. Set the request method to POST
3. Set the URL to `http://127.0.0.1:8000/api/persons/2/unassign_task/` (replace 2 with the ID of a person)
4. Go to the "Body" tab
5. Select "raw" and "JSON" format
6. Enter the following JSON data:
```json
{
    "task_id": 2
}
```
7. Save the request as "Unassign Task from Person"
8. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 2,
    "title": "Practice REST API concepts",
    "description": "",
    "status": "in_progress",
    "priority": 2,
    "due_date": null,
    "completed": false,
    "assigned_to": null,
    "assigned_to_name": null,
    "created_at": "2023-03-15T09:30:00Z",
    "updated_at": "2023-03-15T12:30:00Z"
}
```

### Unassign a Task from a Person (from Task endpoint)

1. Create a new request in your collection
2. Set the request method to POST
3. Set the URL to `http://127.0.0.1:8000/api/tasks/1/unassign_person/` (replace 1 with the ID of a task)
4. Save the request as "Unassign Person from Task"
5. Click "Send" to execute the request

**Expected Response:**
```json
{
    "id": 1,
    "title": "Complete Django REST tutorial",
    "description": "Complete the Django REST framework tutorial and understand the concepts",
    "status": "completed",
    "priority": 1,
    "due_date": "2023-03-20",
    "completed": true,
    "assigned_to": null,
    "assigned_to_name": null,
    "created_at": "2023-03-15T09:00:00Z",
    "updated_at": "2023-03-15T12:45:00Z"
}
```

### View Unassigned Tasks

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/tasks/unassigned_tasks/`
4. Save the request as "List Unassigned Tasks"
5. Click "Send" to execute the request

**Expected Response:**
```json
[
    {
        "id": 1,
        "title": "Complete Django REST tutorial",
        "status": "completed",
        "priority": 1,
        "due_date": "2023-03-20",
        "completed": true,
        "assigned_to_name": null
    },
    {
        "id": 2,
        "title": "Practice REST API concepts",
        "status": "in_progress",
        "priority": 2,
        "due_date": null,
        "completed": false,
        "assigned_to_name": null
    }
]
```

## Custom Actions

### List Completed Tasks

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/tasks/completed_tasks/`
4. Save the request as "List Completed Tasks"
5. Click "Send" to execute the request

**Expected Response:**
```json
[
    {
        "id": 1,
        "title": "Complete Django REST tutorial",
        "status": "completed",
        "priority": 1,
        "due_date": "2023-03-20",
        "completed": true
    }
]
```

### List Pending Tasks

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/tasks/pending_tasks/`
4. Save the request as "List Pending Tasks"
5. Click "Send" to execute the request

**Expected Response:**
```json
[
    {
        "id": 2,
        "title": "Practice REST API concepts",
        "status": "in_progress",
        "priority": 2,
        "due_date": null,
        "completed": false
    }
]
```

## Filtering and Searching

### Filter by Status

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/tasks/?status=in_progress`
4. Save the request as "Filter by Status"
5. Click "Send" to execute the request

### Search by Title or Description

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/tasks/?search=django`
4. Save the request as "Search Tasks"
5. Click "Send" to execute the request

### Order by Priority

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/tasks/?ordering=priority`
4. Save the request as "Order by Priority"
5. Click "Send" to execute the request

### Filter Persons by Department

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/persons/?department=Engineering`
4. Save the request as "Filter Persons by Department"
5. Click "Send" to execute the request

### Search Persons

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/persons/?search=john`
4. Save the request as "Search Persons"
5. Click "Send" to execute the request

### Filter Tasks by Assigned Person

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/tasks/?assigned_to=1` (replace 1 with the ID of a person)
4. Save the request as "Filter Tasks by Assigned Person"
5. Click "Send" to execute the request

### Filter Unassigned Tasks

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://127.0.0.1:8000/api/tasks/?assigned_to__isnull=true`
4. Save the request as "Filter Unassigned Tasks"
5. Click "Send" to execute the request

## Authentication

### Login

1. Create a new request in your collection
2. Set the request method to POST
3. Set the URL to `http://127.0.0.1:8000/api-auth/login/`
4. Go to the "Body" tab
5. Select "x-www-form-urlencoded"
6. Add the following key-value pairs:
   - username: your_username
   - password: your_password
7. Save the request as "Login"
8. Click "Send" to execute the request

### Using Authentication in Requests

For any request that requires authentication:

1. Go to the "Authorization" tab
2. Select "Basic Auth" from the Type dropdown
3. Enter your username and password
4. Click "Send" to execute the request

Alternatively, you can set up environment variables and use them for authentication in your requests.

## Troubleshooting

### Common Issues

1. **"Error: connect ECONNREFUSED 127.0.0.1:8000"**:
   - Make sure the Django development server is running. Start it with:
     ```bash
     python manage.py runserver
     ```
   - Check that you're using the correct URL. The default is `http://127.0.0.1:8000/` (not localhost)
   - Ensure no firewall is blocking the connection

2. **"404 Not Found"**:
   - Verify that you're using the correct URL path
   - Check that the API endpoint exists (refer to API documentation)
   - For ID-specific endpoints, ensure the ID exists in the database

3. **"400 Bad Request"**:
   - Check your JSON format (it should be valid JSON)
   - Ensure all required fields are provided
   - Verify field values match the expected types and constraints

4. **"401 Unauthorized"**:
   - Check your authentication credentials
   - Ensure you're logged in if the endpoint requires authentication

5. **"500 Internal Server Error"**:
   - Check the Django server console for error messages
   - This usually indicates a problem with the server-side code 