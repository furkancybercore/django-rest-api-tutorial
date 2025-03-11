from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    This is used to convert Task instances to JSON and vice versa.
    """
    class Meta:
        model = Task
        fields = '__all__'  # Serializes all fields
        read_only_fields = ('created_at', 'updated_at')  # These fields are read-only


class TaskListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing tasks.
    Shows fewer fields than the complete serializer.
    """
    class Meta:
        model = Task
        fields = ('id', 'title', 'status', 'priority', 'due_date', 'completed') 