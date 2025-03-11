from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Person
from .serializers import (
    TaskSerializer, 
    TaskListSerializer, 
    PersonSerializer, 
    PersonWithTasksSerializer
)

# Create your views here.

class PersonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Person instances.
    
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department']
    search_fields = ['name', 'email', 'department']
    ordering_fields = ['name', 'created_at']
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions:
        - retrieve: Use serializer with tasks
        - other actions: Use the regular serializer
        """
        if self.action == 'retrieve' or self.action == 'tasks':
            return PersonWithTasksSerializer
        return PersonSerializer
    
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
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'completed', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'due_date', 'created_at']
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions:
        - list: Use a simplified serializer
        - other actions: Use the full serializer
        """
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer
    
    @action(detail=False, methods=['get'])
    def completed_tasks(self, request):
        """
        Custom action to list all completed tasks.
        
        URL: /api/tasks/completed_tasks/
        """
        completed_tasks = Task.objects.filter(completed=True)
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_tasks(self, request):
        """
        Custom action to list all pending tasks.
        
        URL: /api/tasks/pending_tasks/
        """
        pending_tasks = Task.objects.filter(completed=False)
        serializer = self.get_serializer(pending_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unassigned_tasks(self, request):
        """
        Custom action to list all unassigned tasks.
        
        URL: /api/tasks/unassigned_tasks/
        """
        unassigned_tasks = Task.objects.filter(assigned_to=None)
        serializer = self.get_serializer(unassigned_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Assign this task to a person.
        
        URL: /api/tasks/{id}/assign/
        """
        task = self.get_object()
        person_id = request.data.get('person_id')
        
        if not person_id:
            return Response(
                {'error': 'person_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response(
                {'error': f'Person with id {person_id} does not exist'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        task.assigned_to = person
        task.save()
        
        return Response(
            {'success': f'Task assigned to {person.name}'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def unassign(self, request, pk=None):
        """
        Unassign this task from its current assignee.
        
        URL: /api/tasks/{id}/unassign/
        """
        task = self.get_object()
        
        if not task.assigned_to:
            return Response(
                {'error': 'Task is not assigned to anyone'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        previous_assignee = task.assigned_to.name
        task.assigned_to = None
        task.save()
        
        return Response(
            {'success': f'Task unassigned from {previous_assignee}'},
            status=status.HTTP_200_OK
        )
