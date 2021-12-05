"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter, SimpleRouter

# для API-документации (библиотека drf_yasg для Swagger)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import UserModelViewSet, UserCustomViewSet, UserListAPIView
from projects.views import ProjectModelViewSet, TodoModelViewSet


# для swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Library",
        default_version='v2',
        description="Documentation to out project",
        contact=openapi.Contact(email="ksn1974@mail.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = DefaultRouter()
# router = SimpleRouter()       # не имеет удобного интерфейса навигации
router.register('users', UserModelViewSet)              # Доступны все методы
router.register('users_restrict', UserCustomViewSet)    # Доступны только (list, Retrieve, Update)
router.register('projects', ProjectModelViewSet)
router.register('todo', TodoModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('test_views/', include('test_views.urls', namespace='test_views'), name='test_views'),
    path('api-token-auth/', obtain_auth_token),
    # Версионность API по URLPathVersioning
    # path('api/<str:version>/users/', UserListAPIView.as_view()),
    # Версионность API по NamespaceVersioning (неудобно - объемный код, меняем url)
    # path('api/users/v1', include('users.urls', namespace='v1')),
    # path('api/users/v2', include('users.urls', namespace='v2')),
    # Версионность по QueryParameterVersioning - подключит автоматически при api/users/?version=v2
    # Версионность по AcceptHeaderVersioning - через Postman в header (application/json; version=v2)

    # API -Documentation
    path('swagger/', schema_view.with_ui('swagger')),           # Swagger
    path('swagger<str:format>/', schema_view.without_ui()),     # вызов в формате, к примеру (/swagger.json)
    path('redoc/', schema_view.with_ui('redoc')),               # аналог Swagger

    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("graphql_no_graph/", csrf_exempt(GraphQLView.as_view(graphiql=False))),

]
