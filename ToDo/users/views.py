from django.shortcuts import render
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserModelSerializer


class UserModelViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]     # Более детальная настройка представления
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

