from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    
    def get_paginated_response(self, data):
        return Response({
            'has_next': self.page.has_next(),
            'has_previous': self.page.has_previous(),
            'count': self.page.paginator.count,
            'results': data
        })
