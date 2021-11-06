from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

import test_views.views as views

app_name = 'test_views'

router = DefaultRouter()
# basename нужен!!! UserViewSet не связан с моделью данных, чтобы DRF смог создать название url-адреса
router.register('users3', views.UserViewSet, basename='user')
router.register('users4', views.UserModelViewSet)
router.register('users_p', views.UserLimitOffsetPaginationViewSet)

filter_router = DefaultRouter()
filter_router.register('fix_filter', views.UserQuerysetFilterViewSet)       # с фиксированным фильтром
filter_router.register('param', views.UserParamFilterViewSet)               # с параметром
filter_router.register('django_filter', views.UserDjangoFilterViewSet)      # через библиотеку django-filter


# router.register('create', views.UserCreateAPIView)
# router.register('view', views.UserRetrieveAPIView)
# router.register('update', views.UserUpdateAPIView)
# router.register('delete', views.UserDestroyAPIView)
# router.register('list', views.UserListAPIView)


urlpatterns = [
    path('api-view/', views.UserAPIVIew.as_view()),
    path('api-view2/', views.user_view),
    path('list/', views.UserListAPIView.as_view()),
    path('create/', views.UserCreateAPIView.as_view()),
    path('view/<int:pk>/', views.UserRetrieveAPIView.as_view()),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view()),
    path('delete/<int:pk>/', views.UserDestroyAPIView.as_view()),
    path('router/', include(router.urls)),
    path('filters/kwargs/<str:name>/', views.UserKwargsFilterView.as_view()),   # параметр в URL
    path('router_filter/', include(filter_router.urls)),


    #
    # path('add/<int:pk>/', basket_add, name='add'),
    # path('remove/<int:pk>/', basket_remove, name='remove'),
    # path('edit/<int:pk>/<int:quantity>/', basket_edit, name='edit')
]

