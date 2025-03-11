from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task, Person

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

class PersonProfileUpdateTests(APITestCase):
    """
    Test cases for the Person profile update functionality.
    """
    def setUp(self):
        """
        Set up test data including a user for authentication.
        """
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        
        # Create test persons
        self.person1 = Person.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            phone="+1234567890",
            department="Engineering"
        )
        
        self.person2 = Person.objects.create(
            name="Jane Smith",
            email="jane.smith@example.com",
            phone="+0987654321",
            department="Marketing"
        )
        
        # Setup client with authentication
        self.client = APIClient()
    
    def test_profile_update_requires_authentication(self):
        """
        Test that profile update requires authentication.
        """
        url = reverse('person-profile-update', args=[self.person1.id])
        data = {
            'name': 'John Doe Updated',
            'email': 'john.updated@example.com'
        }
        
        # Try without authentication
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Now authenticate and try again
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_profile_full(self):
        """
        Test updating a person's full profile.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('person-profile-update', args=[self.person1.id])
        data = {
            'name': 'John Doe Updated',
            'email': 'john.updated@example.com',
            'confirm_email': 'john.updated@example.com',
            'phone': '+1111222333',
            'department': 'Software Development'
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        
        # Verify the database was updated
        self.person1.refresh_from_db()
        self.assertEqual(self.person1.name, 'John Doe Updated')
        self.assertEqual(self.person1.email, 'john.updated@example.com')
        self.assertEqual(self.person1.department, 'Software Development')
    
    def test_update_profile_partial(self):
        """
        Test partially updating a person's profile with PATCH.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('person-profile-update', args=[self.person1.id])
        data = {
            'department': 'Research & Development'
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify only the specified field was updated
        self.person1.refresh_from_db()
        self.assertEqual(self.person1.name, 'John Doe')  # Unchanged
        self.assertEqual(self.person1.email, 'john.doe@example.com')  # Unchanged
        self.assertEqual(self.person1.department, 'Research & Development')  # Changed
    
    def test_email_uniqueness_validation(self):
        """
        Test that email uniqueness is enforced.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('person-profile-update', args=[self.person1.id])
        
        # Try to update with an email that's already used by another person
        data = {
            'email': 'jane.smith@example.com',  # This email is used by person2
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['errors'])
    
    def test_email_confirmation_validation(self):
        """
        Test that email confirmation validation works.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('person-profile-update', args=[self.person1.id])
        
        # Try to update with mismatched email and confirm_email
        data = {
            "name": "John Doe",  # Required field for PUT requests
            "email": "john.new@example.com",
            "confirm_email": "john.different@example.com"
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_email', response.data['errors'])
    
    def test_name_validation(self):
        """
        Test that name validation works.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('person-profile-update', args=[self.person1.id])
        
        # Try to update with a name that's too short
        data = {
            'name': 'J'  # Too short (less than 2 characters)
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['errors'])
