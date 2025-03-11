#!/usr/bin/env python
"""
Script to populate the database with sample data.
Run this script with:
    python manage.py shell < create_sample_data.py
"""

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
    {
        'title': 'Master Django REST Framework',
        'description': 'Learn serializers, viewsets, and authentication in DRF',
        'status': 'in_progress',
        'priority': 2,
        'due_date': datetime.date.today() + datetime.timedelta(days=2),
        'completed': False
    },
    {
        'title': 'Build a RESTful API',
        'description': 'Create a complete REST API with proper documentation',
        'status': 'pending',
        'priority': 3,
        'due_date': datetime.date.today() + datetime.timedelta(days=7),
        'completed': False
    },
    {
        'title': 'Test API with Postman',
        'description': 'Use Postman to test all API endpoints',
        'status': 'pending',
        'priority': 4,
        'due_date': datetime.date.today() + datetime.timedelta(days=8),
        'completed': False
    },
    {
        'title': 'Deploy API to Production',
        'description': 'Deploy the REST API to a production server',
        'status': 'pending',
        'priority': 5,
        'due_date': datetime.date.today() + datetime.timedelta(days=14),
        'completed': False
    },
]

# Save tasks to database
for task_data in tasks:
    task = Task(**task_data)
    task.save()
    print(f"Created task: {task.title}")

print(f"Successfully created {len(tasks)} sample tasks!") 