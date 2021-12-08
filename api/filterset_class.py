from django_filters import rest_framework as filtersS  
from main.models import Service ,Request
from account.models import User


class ServiceFilter(filtersS.FilterSet):
    min_price = filtersS.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filtersS.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Service
        fields = ['min_price', 'max_price']


class RequestFilter(filtersS.FilterSet):
    min_price = filtersS.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filtersS.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Request
        fields = ['min_price', 'max_price']

