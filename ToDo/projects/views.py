from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer, StaticHTMLRenderer, \
    TemplateHTMLRenderer

from rest_framework.viewsets import ModelViewSet

from .filters import ProjectFilter, TodoFilter
from .serializers import ProjectModelSerializer, ProjectModelSerializerExt, TodoModelSerializer, TodoModelSerializerV2
from .models import Project, Todo

#*********************************************************
# Pagination
#*********************************************************
class ProjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20


class TodoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20


class ProjectModelViewSet(ModelViewSet):
    queryset = Project.objects.all()
    # serializer_class = ProjectModelSerializer
    pagination_class = ProjectLimitOffsetPagination
    filterset_class = ProjectFilter         # Filtering через библиотеку django-filter

    def get_serializer_class(self):
        if self.request.method in ['GET']:      # Для GET-запросов будем брать др. серилизатор
            return ProjectModelSerializerExt
        return ProjectModelSerializer


class TodoModelViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoModelSerializer
    pagination_class = TodoLimitOffsetPagination
    # filterset_fields = ['project']
    filterset_class = TodoFilter

    def get_serializer_class(self):
        if hasattr(self.request, 'version') and self.request.version == 'v2':   # если версия передана и =='v2'
            return TodoModelSerializerV2
        return TodoModelSerializer

    def perform_create(self, serializer):
        serializer.save(is_active=True)         # при создании ставим активность заметки, не смотря на поле