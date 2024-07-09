import math

from asgiref.sync import async_to_sync
from rest_framework import pagination
from rest_framework.response import Response

from .responses import SocketSuccessResponse


class MyPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'next': int(self.page.next_page_number()) if self.page.paginator.num_pages > self.page.number else None,
            'previous': int(self.page.previous_page_number()) if self.page.number > 1 else None,
            'page_size': self.page_size,
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class PaginationView:
    pagination_class = MyPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class SocketPaginationView:
    page_size = 10
    page = 1

    def get_page_numbers(self):
        self.page_size = int(self.query_params.get('page_size', self.page_size))
        self.page = int(self.query_params.get('page', self.page))

    def pagination_queryset(self, queryset):
        self.get_page_numbers()

        offset = abs(self.page - 1) * self.page_size

        self.total_count = queryset.count()
        self.total_pages = math.ceil(self.total_count / self.page_size)

        queryset = queryset[offset:offset + self.page_size]

        return queryset

    def get_pagination_response(self, queryset):
        return SocketSuccessResponse(
            next=self.page + 1 if (self.page + 1) <= self.total_pages else None,
            previous=self.page - 1 if (self.page - 1) >= 1 else None,
            current_page=self.page,
            page_size=self.page_size,
            count=self.total_count,
            total_pages=self.total_pages,
            results=queryset
        )

    def send_pagination_response(self, queryset, action, serializer=None):
        if serializer:
            queryset = serializer(self.pagination_queryset(queryset), many=True).data

        async_to_sync(self.send)(SocketSuccessResponse(
            action=action,
            next=self.page + 1 if (self.page + 1) <= self.total_pages else None,
            previous=self.page - 1 if (self.page - 1) >= 1 else None,
            current_page=self.page,
            page_size=self.page_size,
            count=self.total_count,
            total_pages=self.total_pages,
            results=queryset
        ))
