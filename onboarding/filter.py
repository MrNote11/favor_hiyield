import django_filters
from .models import Customeruser
from django.db.models import Q

class CustomerUserFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date_joined", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="date_joined", lookup_expr='lte')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Customeruser
        fields = ['start_date', 'end_date']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(username__icontains=value) | Q(email__icontains=value)
        )