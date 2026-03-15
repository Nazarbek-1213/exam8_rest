import django_filters
from .models import Project


class ProjectFilter(django_filters.FilterSet):
    budget_min = django_filters.NumberFilter(field_name='budget', lookup_expr='gte')
    budget_max = django_filters.NumberFilter(field_name='budget', lookup_expr='lte')
    status = django_filters.ChoiceFilter(choices=Project.STATUS_CHOICES)
    deadline_before = django_filters.DateFilter(field_name='deadline', lookup_expr='lte')
    deadline_after = django_filters.DateFilter(field_name='deadline', lookup_expr='gte')

    class Meta:
        model = Project
        fields = ['status', 'budget_min', 'budget_max', 'deadline_before', 'deadline_after']
