from rest_framework import serializers
from .models import Task, Person

class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Person model.
    This is used to convert Person instances to JSON and vice versa.
    """
    class Meta:
        model = Person
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PersonWithTasksSerializer(serializers.ModelSerializer):
    """
    Serializer for the Person model that includes their assigned tasks.
    """
    assigned_tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_assigned_tasks(self, obj):
        # Get simplified task representation
        tasks = obj.assigned_tasks.all()
        return TaskListSerializer(tasks, many=True).data


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    This is used to convert Task instances to JSON and vice versa.
    """
    assigned_to_name = serializers.ReadOnlyField(source='assigned_to.name')
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class TaskListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing tasks.
    Shows fewer fields than the complete serializer.
    """
    assigned_to_name = serializers.ReadOnlyField(source='assigned_to.name')
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'status', 'priority', 'due_date', 'completed', 'assigned_to_name') 