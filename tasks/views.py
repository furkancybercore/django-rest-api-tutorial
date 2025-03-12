from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Person
from .serializers import (
    TaskSerializer, 
    TaskListSerializer, 
    PersonSerializer, 
    PersonWithTasksSerializer,
    ProfileUpdateSerializer
)

# Create your views here.

class PersonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Person instances.
    
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    
    BEGINNER'S GUIDE TO THIS CLASS:
    -------------------------------
    Just like TaskViewSet, this is a Django REST Framework ViewSet that handles
    different HTTP methods for managing Person objects:
    
    - GET /api/persons/ -> list (show all persons)
    - POST /api/persons/ -> create (add a new person)
    - GET /api/persons/1/ -> retrieve (show person with id=1)
    - PUT/PATCH /api/persons/1/ -> update (modify person with id=1)
    - DELETE /api/persons/1/ -> destroy (delete person with id=1)
    
    The PersonViewSet also includes custom actions for working with tasks
    assigned to persons and for updating profiles with special validation.
    """
    # This defines which database objects this ViewSet will work with
    queryset = Person.objects.all()
    
    # This defines which serializer class to use by default
    serializer_class = PersonSerializer
    
    # These define how filtering, searching, and ordering work
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Which fields can be filtered by exact value
    # Example: /api/persons/?department=Engineering
    filterset_fields = ['department']
    
    # Which fields can be searched with text
    # Example: /api/persons/?search=john
    search_fields = ['name', 'email', 'department']
    
    # Which fields can be used for ordering
    # Example: /api/persons/?ordering=name
    ordering_fields = ['name', 'created_at']
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions:
        - retrieve: Use serializer with tasks
        - profile_update: Use profile update serializer
        - other actions: Use the regular serializer
        
        EXPLANATION:
        ------------
        This method customizes which serializer to use based on the current action:
        
        1. For 'retrieve' (viewing a single person) or 'tasks' (viewing tasks):
           - Uses PersonWithTasksSerializer which includes the tasks assigned to that person
           - This is helpful for seeing details about a person and their tasks in one request
        
        2. For 'profile_update' (custom action to update profile):
           - Uses ProfileUpdateSerializer which includes special validation rules
           - This provides extra checks when updating sensitive information
        
        3. For all other actions (list, create, etc.):
           - Uses the default PersonSerializer which has basic person information
           - This keeps the data simple and lightweight when full details aren't needed
        
        This approach lets us reuse the same ViewSet but with different serialization
        behavior depending on what information is most appropriate for each action.
        """
        if self.action == 'retrieve' or self.action == 'tasks':
            return PersonWithTasksSerializer
        elif self.action == 'profile_update':
            return ProfileUpdateSerializer
        return PersonSerializer
    
    @action(detail=True, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def profile_update(self, request, pk=None):
        """
        Update a person's profile with validation.
        
        This endpoint requires authentication and provides extra validation
        for profile fields like email and name.
        
        URL: /api/persons/{id}/profile_update/
        Method: PUT or PATCH
        
        EXPLANATION:
        ------------
        This is a custom action that creates an endpoint at /api/persons/1/profile_update/
        
        The @action decorator creates this special endpoint:
        - detail=True means it works on a specific person (not the collection)
        - methods=['put', 'patch'] means it accepts both PUT (full update) and PATCH (partial update)
        - permission_classes=[IsAuthenticated] means only logged-in users can access it
        
        The method does the following:
        
        1. self.get_object() retrieves the Person instance by ID from the URL
           - This uses the same lookup logic as other ViewSet methods
        
        2. self.get_serializer(...) creates a ProfileUpdateSerializer instance
           - person: The object to update
           - data: The data from the request
           - partial: True for PATCH (only update provided fields), False for PUT (update all fields)
        
        3. serializer.is_valid() checks if the data meets validation requirements
           - The ProfileUpdateSerializer defines special rules like email uniqueness
        
        4. If valid, serializer.save() updates the person in the database
           - Then returns a success response with the updated data
        
        5. If invalid, returns an error response with details about what failed
           - This helps the client understand what needs to be fixed
        
        This pattern provides a specialized update endpoint with additional validation
        beyond what the standard update methods provide.
        """
        person = self.get_object()
        serializer = self.get_serializer(person, data=request.data, partial=self.request.method == 'PATCH')
        
        if serializer.is_valid():
            # If data is valid, save the changes to the database
            serializer.save()
            
            # Return a successful response with helpful details
            return Response(
                {
                    "status": "success",  # Clear status indicator
                    "message": "Profile updated successfully",  # Human-readable message
                    "data": serializer.data  # The updated data after saving
                }, 
                status=status.HTTP_200_OK  # HTTP 200 success status code
            )
        
        # If data validation failed, return an error response
        return Response(
            {
                "status": "error",  # Clear error indicator
                "message": "Profile update failed",  # Human-readable message
                "errors": serializer.errors  # Detailed validation errors from the serializer
            },
            status=status.HTTP_400_BAD_REQUEST  # HTTP 400 bad request status code
        )
    
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """
        Get all tasks assigned to a specific person.
        
        URL: /api/persons/{id}/tasks/
        """
        person = self.get_object()
        serializer = PersonWithTasksSerializer(person)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign_task(self, request, pk=None):
        """
        Assign a task to this person.
        
        URL: /api/persons/{id}/assign_task/
        """
        person = self.get_object()
        task_id = request.data.get('task_id')
        
        if not task_id:
            return Response(
                {'error': 'task_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {'error': f'Task with id {task_id} does not exist'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        task.assigned_to = person
        task.save()
        
        return Response(
            {'success': f'Task "{task.title}" assigned to {person.name}'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def unassign_task(self, request, pk=None):
        """
        Unassign a task from this person.
        
        URL: /api/persons/{id}/unassign_task/
        """
        person = self.get_object()
        task_id = request.data.get('task_id')
        
        if not task_id:
            return Response(
                {'error': 'task_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {'error': f'Task with id {task_id} does not exist'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if task.assigned_to != person:
            return Response(
                {'error': f'Task is not assigned to {person.name}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.assigned_to = None
        task.save()
        
        return Response(
            {'success': f'Task "{task.title}" unassigned from {person.name}'},
            status=status.HTTP_200_OK
        )

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Task instances.
    
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    
    BEGINNER'S GUIDE TO THIS CLASS:
    -------------------------------
    A ViewSet is a Django REST Framework class that handles different HTTP methods
    (GET, POST, PUT, DELETE) and maps them to appropriate actions:
    
    - GET /api/tasks/ -> list (show all tasks)
    - POST /api/tasks/ -> create (make a new task)
    - GET /api/tasks/1/ -> retrieve (show task with id=1)
    - PUT/PATCH /api/tasks/1/ -> update (modify task with id=1)
    - DELETE /api/tasks/1/ -> destroy (delete task with id=1)
    
    The ModelViewSet automatically implements all these actions for you.
    """
    # This defines which database objects this ViewSet will work with
    # Task.objects.all() means "get all Task objects from the database"
    queryset = Task.objects.all()
    
    # This defines which serializer class to use by default
    # Serializers convert between Django model instances and JSON
    serializer_class = TaskSerializer
    
    # These define how filtering, searching, and ordering work
    # They let you do things like /api/tasks/?status=completed or /api/tasks/?search=django
    filter_backends = [
        DjangoFilterBackend,  # Enables filtering by exact values
        filters.SearchFilter,  # Enables text search across fields
        filters.OrderingFilter  # Enables ordering by fields
    ]
    
    # Which fields can be filtered by exact value
    # Example: /api/tasks/?status=completed&priority=1
    filterset_fields = ['status', 'priority', 'completed', 'assigned_to']
    
    # Which fields can be searched with text
    # Example: /api/tasks/?search=django
    search_fields = ['title', 'description']
    
    # Which fields can be used for ordering
    # Example: /api/tasks/?ordering=-due_date (minus sign means descending)
    ordering_fields = ['priority', 'due_date', 'created_at']
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions:
        - list: Use a simplified serializer
        - other actions: Use the full serializer
        
        EXPLANATION:
        ------------
        This method decides which serializer to use based on the current action.
        For the list view (showing all tasks), we use TaskListSerializer which
        typically includes fewer fields for better performance and readability.
        
        For individual task views or other actions, we use the full TaskSerializer
        which includes all fields and details.
        """
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer
    
    @action(detail=False, methods=['get'])
    def completed_tasks(self, request):
        """
        Custom action to list all completed tasks.
        
        URL: /api/tasks/completed_tasks/
        
        EXPLANATION:
        ------------
        This creates a custom endpoint at /api/tasks/completed_tasks/
        The @action decorator creates this custom endpoint:
        - detail=False means it acts on the collection (not a specific task)
        - methods=['get'] means it only responds to GET requests
        
        Inside the method:
        1. We filter the tasks to only include completed ones
        2. We serialize the data (convert to JSON)
        3. We return a Response with the serialized data
        """
        completed_tasks = Task.objects.filter(completed=True)
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_tasks(self, request):
        """
        Custom action to list all pending tasks.
        
        URL: /api/tasks/pending_tasks/
        
        EXPLANATION:
        ------------
        Similar to completed_tasks, but filters for non-completed tasks.
        """
        pending_tasks = Task.objects.filter(completed=False)
        serializer = self.get_serializer(pending_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unassigned_tasks(self, request):
        """
        Custom action to list all unassigned tasks.
        
        URL: /api/tasks/unassigned_tasks/
        
        EXPLANATION:
        ------------
        Similar to the other custom endpoints, but filters for tasks
        where assigned_to is None (meaning no person is assigned).
        """
        unassigned_tasks = Task.objects.filter(assigned_to=None)
        serializer = self.get_serializer(unassigned_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Assign this task to a person.
        
        URL: /api/tasks/{id}/assign/
        
        EXPLANATION:
        ------------
        This creates a custom endpoint at /api/tasks/1/assign/
        The @action decorator creates this custom endpoint:
        - detail=True means it acts on a specific task (not the collection)
        - methods=['post'] means it only responds to POST requests
        
        The method:
        1. Gets the task object using self.get_object()
        2. Gets the person_id from the request data
        3. Validates the input and finds the person
        4. Assigns the person to the task
        5. Returns a success response
        """
        task = self.get_object()
        person_id = request.data.get('person_id')
        
        # Input validation - check if person_id was provided
        if not person_id:
            return Response(
                {'error': 'person_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to find the person in the database
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response(
                {'error': f'Person with id {person_id} does not exist'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update the task's assigned_to field and save to database
        task.assigned_to = person
        task.save()
        
        # Return a success response
        return Response(
            {'success': f'Task assigned to {person.name}'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def unassign(self, request, pk=None):
        """
        Unassign this task from its current assignee.
        
        URL: /api/tasks/{id}/unassign/
        
        EXPLANATION:
        ------------
        This creates a custom endpoint at /api/tasks/1/unassign/
        Similar to the assign method, but removes assignment instead.
        
        The method:
        1. Gets the task object using self.get_object()
        2. Checks if the task is currently assigned
        3. Removes the assignment by setting assigned_to to None
        4. Returns a success response
        """
        task = self.get_object()
        
        # Check if the task is already unassigned
        if not task.assigned_to:
            return Response(
                {'error': 'Task is not assigned to anyone'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Store the previous assignee's name for the response message
        previous_assignee = task.assigned_to.name
        
        # Update the task to be unassigned and save to database
        task.assigned_to = None
        task.save()
        
        # Return a success response
        return Response(
            {'success': f'Task unassigned from {previous_assignee}'},
            status=status.HTTP_200_OK
        )
