from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

# Create your tests here.

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
        self.task2 = Task.objects.create(
            title="Test Task 2",
            description="This is another test task",
            status="in_progress",
            priority=2
        )
        self.task3 = Task.objects.create(
            title="Test Task 3",
            description="This is a completed test task",
            status="completed",
            priority=3,
            completed=True
        )
    
    def test_get_tasks_list(self):
        """
        Test retrieving a list of tasks.
        """
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_create_task(self):
        """
        Test creating a new task.
        """
        url = reverse('task-list')
        data = {
            'title': 'New Test Task',
            'description': 'This is a new test task',
            'status': 'pending',
            'priority': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(Task.objects.get(title='New Test Task').description, 'This is a new test task')
    
    def test_get_task_detail(self):
        """
        Test retrieving a specific task.
        """
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task 1')
    
    def test_update_task(self):
        """
        Test updating a task.
        """
        url = reverse('task-detail', args=[self.task1.id])
        data = {
            'title': 'Updated Test Task',
            'description': 'This is an updated test task',
            'status': 'in_progress',
            'priority': 2
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Test Task')
        self.assertEqual(self.task1.status, 'in_progress')
    
    def test_delete_task(self):
        """
        Test deleting a task.
        """
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)
    
    def test_completed_tasks_filter(self):
        """
        Test filtering completed tasks.
        """
        url = reverse('task-completed-tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task 3')
    
    def test_pending_tasks_filter(self):
        """
        Test filtering pending tasks.
        """
        url = reverse('task-pending-tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn(response.data[0]['title'], ['Test Task 1', 'Test Task 2'])
