from django.contrib import admin
from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['freelancer', 'project', 'price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['freelancer__username', 'project__title']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
