from django_filters import rest_framework as filtersS  
from main.models import  Request
from account.models import User




class RequestFilter(filtersS.FilterSet):
    min_price = filtersS.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filtersS.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Request
        fields = ['min_price', 'max_price']

