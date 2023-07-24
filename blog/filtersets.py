
from django_filters import rest_framework as filtersS  
from .models import Blog


class BlogFilter(filtersS.FilterSet):

    class Meta:
        model = Blog
        fields = ['category',]