from django.contrib import admin
from .models import Task, Person

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface for the Task model.
    """
    list_display = ('title', 'status', 'priority', 'due_date', 'completed', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'completed', 'assigned_to')
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
        ('Assignment', {
            'fields': ('assigned_to',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """
    Admin interface for the Person model.
    """
    list_display = ('name', 'email', 'phone', 'department', 'created_at')
    list_filter = ('department',)
    search_fields = ('name', 'email', 'department')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Organizational Information', {
            'fields': ('department',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
