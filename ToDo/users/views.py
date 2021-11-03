from django.shortcuts import render
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer, StaticHTMLRenderer, \
    TemplateHTMLRenderer

from rest_framework.viewsets import ModelViewSet
from .serializers import UserModelSerializer
from .models import User


class UserModelViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]     # Более детальная настройка представления
    # renderer_classes = [AdminRenderer]    # Выглядит прикольно, но пеерстает работать React на фронте (рендерит ерунду)
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

