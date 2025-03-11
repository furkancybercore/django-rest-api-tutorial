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


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a person's profile.
    Includes specific validations for profile data.
    """
    confirm_email = serializers.EmailField(write_only=True, required=False)
    
    class Meta:
        model = Person
        fields = ('name', 'email', 'confirm_email', 'phone', 'department')
        
    def validate_name(self, value):
        """
        Validate that the name is not too short and contains valid characters.
        """
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value
    
    def validate_email(self, value):
        """
        Validate that the email is unique.
        """
        # Get current instance (if any)
        instance = getattr(self, 'instance', None)
        
        # If this is an update (instance exists) and email hasn't changed, skip validation
        if instance and instance.email == value:
            return value
            
        # Check if there's another person with this email
        if Person.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
    def validate(self, data):
        """
        Validate that confirm_email matches email if provided.
        """
        email = data.get('email')
        confirm_email = data.pop('confirm_email', None)
        
        # If confirm_email was provided, check if it matches email
        if confirm_email is not None:
            if email != confirm_email:
                raise serializers.ValidationError({"confirm_email": "Email addresses do not match."})
        
        return data


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