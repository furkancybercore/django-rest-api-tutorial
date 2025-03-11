from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer, TaskListSerializer

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Task instances.
    
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'completed']
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
