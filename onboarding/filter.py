import django_filters
from .models import Customeruser
from django.db.models import Q

class CustomerUserFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date_joined", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="date_joined", lookup_expr='lte')
    search = django_filters.CharFilter(method='filter_search')
    blacklist = django_filters.BooleanFilter(field_name="blacklist")

    class Meta:
        model = Customeruser
        fields = ['blacklist','start_date', 'end_date','search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(username__icontains=value) | Q(email__icontains=value)
        )