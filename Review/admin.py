from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'freelancer', 'rating', 'contract', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reviewer__username', 'freelancer__username', 'comment']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
