import django_filters
from django.db import models
from .models import Member


class MemberFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_name')
    joined_after = django_filters.DateFilter(field_name='joined_date', lookup_expr='gte')
    joined_before = django_filters.DateFilter(field_name='joined_date', lookup_expr='lte')

    class Meta:
        model = Member
        fields = ['is_active']

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )
