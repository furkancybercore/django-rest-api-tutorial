# Postman Guide for Task Manager API

This guide will help you test the Task Manager API using Postman.

## Table of Contents
1. [Setting Up Postman](#setting-up-postman)
2. [Creating a Collection](#creating-a-collection)
3. [Basic CRUD Operations](#basic-crud-operations)
4. [Custom Actions](#custom-actions)
5. [Filtering and Searching](#filtering-and-searching)
6. [Authentication](#authentication)

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
3. Set the URL to `http://localhost:8000/api/tasks/`
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
3. Set the URL to `http://localhost:8000/api/tasks/`
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
3. Set the URL to `http://localhost:8000/api/tasks/1/` (replace 1 with the ID of a task)
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
3. Set the URL to `http://localhost:8000/api/tasks/1/` (replace 1 with the ID of a task)
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
3. Set the URL to `http://localhost:8000/api/tasks/2/` (replace 2 with the ID of a task)
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
3. Set the URL to `http://localhost:8000/api/tasks/3/` (replace 3 with the ID of a task)
4. Save the request as "Delete Task"
5. Click "Send" to execute the request

**Expected Response:**
- Status code: 204 No Content
- No response body

## Custom Actions

### List Completed Tasks

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://localhost:8000/api/tasks/completed_tasks/`
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
3. Set the URL to `http://localhost:8000/api/tasks/pending_tasks/`
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
3. Set the URL to `http://localhost:8000/api/tasks/?status=in_progress`
4. Save the request as "Filter by Status"
5. Click "Send" to execute the request

### Search by Title or Description

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://localhost:8000/api/tasks/?search=django`
4. Save the request as "Search Tasks"
5. Click "Send" to execute the request

### Order by Priority

1. Create a new request in your collection
2. Set the request method to GET
3. Set the URL to `http://localhost:8000/api/tasks/?ordering=priority`
4. Save the request as "Order by Priority"
5. Click "Send" to execute the request

## Authentication

### Login

1. Create a new request in your collection
2. Set the request method to POST
3. Set the URL to `http://localhost:8000/api-auth/login/`
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