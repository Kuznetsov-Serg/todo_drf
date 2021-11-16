from django.shortcuts import render
from rest_framework import mixins, viewsets, permissions
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer, StaticHTMLRenderer, \
    TemplateHTMLRenderer

from rest_framework.viewsets import ModelViewSet
from .serializers import UserModelSerializer
from .models import User


class UserModelViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]     # Более детальная настройка представления
    # renderer_classes = [AdminRenderer]    # Выглядит прикольно, но перестает работать React на фронте (рендерит ерунду)
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # permission_classes = [permissions.IsAuthenticated]


#*********************************************************
# level 5 (Custom ViewSet)
# часто используется при необходимости только части методов для API
# модель User:  есть возможность просмотра списка и каждого пользователя в отдельности, можно вносить изменения,
#               нельзя удалять и создавать;
#
# class ModelViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet):
#*********************************************************
class UserCustomViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

