from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'budget', 'deadline', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'deadline']
    search_fields = ['title', 'description', 'client__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Project Info', {'fields': ('title', 'description', 'client')}),
        ('Details', {'fields': ('budget', 'deadline', 'status')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
