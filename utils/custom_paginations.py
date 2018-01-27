from collections import OrderedDict
from urllib import parse

from rest_framework import response
from rest_framework.pagination import PageNumberPagination


class CustomPaginationClass(PageNumberPagination):
    """ custom pagi naton class for the app"""
    page_size_query_param = "page_size"

    def get_next_string(self):
        query_dict = parse.parse_qs(parse.urlparse(self.get_next_link()).query)
        for key in query_dict:
            query_dict[key] = ",".join(query_dict[key])
        next_string = parse.urlencode(query_dict)
        return next_string

    def get_previous_string(self):
        
        query_dict = parse.parse_qs(parse.urlparse(self.get_previous_link()).query)
        for key in query_dict:
            query_dict[key] = ",".join(query_dict[key])
        previous_string = parse.urlencode(query_dict)
        return previous_string

    def get_paginated_response(self, data):
        page_info = {
            'resultsPerPage': self.get_page_size(self.request),
            'totalResults': self.page.paginator.count
        }

        return response.Response(OrderedDict([
            ('next', self.page.next_page_number() if self.page.has_next() else None),
            ('previous', self.page.previous_page_number() if self.page.has_previous() else None),
            ('next_string', self.get_next_string()),
            ('previous_string', self.get_previous_string()),
            ('pageInfo', page_info),
            ('results', data)
        ]))
