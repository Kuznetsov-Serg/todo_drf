from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes, action
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination

from users.models import User
from users.serializers import UserModelSerializer
from projects.models import Project, Todo
from projects.serializers import ProjectModelSerializer, TodoModelSerializer
from .filters import UserFilter




#*********************************************************
# level 1 (APIView)
#*********************************************************
# через Класс
class UserAPIVIew(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserModelSerializer(users, many=True)
        return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #     pass

# Через функцию под декораторами
@api_view(['GET', 'POST'])      # POST
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def user_view(request):
    users = User.objects.all()
    serializer = UserModelSerializer(users, many=True)
    return Response(serializer.data)
    # return Response({'test': 1})     # Пример с произвольным словарем в качестве ответа


#*********************************************************
# level 2 (Generic views)
#*********************************************************
# Создать
class UserCreateAPIView(CreateAPIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

# список
class UserListAPIView(ListAPIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

# детализация записи
class UserRetrieveAPIView(RetrieveAPIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

# Удалить
class UserDestroyAPIView(DestroyAPIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

# Изменить
class UserUpdateAPIView(UpdateAPIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


#*********************************************************
# level 3 (ViewSet)
# используется НЕчасто для нестандартных задач и нескольких типов rest-запросов
#*********************************************************
class UserViewSet(viewsets.ViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def list(self, request):
        users = User.objects.all()
        serializer = UserModelSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserModelSerializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])       # detail - работаем ли мы со всей выборкой или с одним объектом
    def first_name_only(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        return Response({'user.first_name': user.first_name})


#*********************************************************
# level 4 (ModelViewSet) - самый простой способ
# часто используется, когда нужно большинство методов для одной модели данных
#*********************************************************
class UserModelViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


#*********************************************************
# level 5 (Custom ViewSet)
# часто используется при необходимости только части методов для API
#*********************************************************
class UserCustomViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                           mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


#*********************************************************
# Filtering
#*********************************************************
# фиксированная строка фильтра
class UserQuerysetFilterViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(username__contains='ivan')


# через kwargs - позиционный параметр в URL
class UserKwargsFilterView(ListAPIView):
    serializer_class = UserModelSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        return User.objects.filter(username__contains=name)


# через именованный параметр
class UserParamFilterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', '')
        users = User.objects.all()
        if name:
            users = users.filter(username__contains=name)
        return users

# через библиотеку django-filter
class UserDjangoFilterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # filterset_fields = ['username', 'first_name']   # полное соответствие фильтру (удобнее по lookup_expr='contains')
    filterset_class = UserFilter


#*********************************************************
# Pagination
#*********************************************************
class UserLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 4


class UserLimitOffsetPaginationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    pagination_class = UserLimitOffsetPagination

