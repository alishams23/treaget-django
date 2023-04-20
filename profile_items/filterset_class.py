from django_filters import rest_framework as filtersS  
from .models import Services
from account.models import User


class ServiceFilter(filtersS.FilterSet):
    min_price = filtersS.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filtersS.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Services
        fields = ['min_price', 'max_price']



