# Postman Guide for Task Manager API

This guide will help you test the Task Manager API using Postman.

## Table of Contents
1. [Before You Begin](#before-you-begin)
2. [Setting Up Postman](#setting-up-postman)
3. [Creating a Collection](#creating-a-collection)
4. [Basic CRUD Operations](#basic-crud-operations)
5. [Custom Actions](#custom-actions)
6. [Filtering and Searching](#filtering-and-searching)
7. [Authentication](#authentication)
8. [Troubleshooting](#troubleshooting)

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

## Basic CRUD Operations

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