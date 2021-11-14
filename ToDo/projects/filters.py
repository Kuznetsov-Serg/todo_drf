from django_filters import rest_framework as filters, IsoDateTimeFilter, DateFilter, DateTimeFilter
from django.db import models

from .models import Project, Todo


class ProjectFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Project
        fields = ['name']


class TodoFilter(filters.FilterSet):
    # created = filters.IsoDateTimeFromToRangeFilter()    # Интервал с часами минутами (DateTime)
    # created = filters.DateRangeFilter()                 # Интервал названием (today, yesterday,..., this year)
    created = filters.DateFromToRangeFilter()           # интервал дат (самый удобный)

    class Meta:
        model = Todo
        fields = ['project', 'created']

# Старый способ с переопределением...
# class TodoFilter(filters.FilterSet):
#     class Meta:
#         model = Todo
#         fields = {
#             # 'project': 'equal',
#             'created': ('gte', 'lte')   # lte (<=), gte (>=)
#         }
#
#     filter_overrides = {
#         models.DateTimeField: {
#             'filter_class': DateTimeFilter   # DateFilter, DateTimeFilter, IsoDateTimeFilter,
#         },
#         'extra': lambda f: {
#              'lookup_expr': 'icontains',
#         },
#     }