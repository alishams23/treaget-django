from rest_framework import pagination

class MyPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size' 
    max_page_size = 200
    last_page_strings = ('the_end',)


