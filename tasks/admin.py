from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface for the Task model.
    """
    list_display = ('title', 'status', 'priority', 'due_date', 'completed', 'created_at')
    list_filter = ('status', 'priority', 'completed')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Status Information', {
            'fields': ('status', 'priority', 'due_date', 'completed')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
