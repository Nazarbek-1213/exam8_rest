from django.contrib import admin
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['project', 'client', 'freelancer', 'agreed_price', 'status', 'created_at', 'finished_at']
    list_filter = ['status', 'created_at']
    search_fields = ['project__title', 'client__username', 'freelancer__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'finished_at']
