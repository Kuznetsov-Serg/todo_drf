from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APISimpleTestCase, APITestCase
from mixer.backend.django import mixer
# from django.contrib.auth.models import User

from .views import UserModelViewSet
from .models import User


class TestUserViewSet(TestCase):
    url = '/api/users/'

    # Подготовка к тестам (данные,...)
    # Повторяющийся код тестов можно вынести в метод setUp
    # Установки запускаются перед каждым тестом
    def setUp(self) -> None:
        pass

    def test_get_list(self):
        # APIRequestFactory (фабрика для создания запросов, используется редко) - для изолированной проверки View
        # (не учитывает URL и на делает реальных запросов)
        factory = APIRequestFactory()  # создать объект класса
        request = factory.get(self.url)  # определяем адрес и метод отправки запроса
        # указываем тип запроса для ModelViewSet и способ (create, destroy, list, update)
        view = UserModelViewSet.as_view({'get': 'list'})
        response = view(request)  # передаем во view и получаем ответ
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_guest(self):
        factory = APIRequestFactory()
        request = factory.post(self.url, {'first_name': 'Иван', 'last_name': 'Иванов', 'password': 'qazwsx123',
                                          'email': 'mail@mail.ru'}, format='json')
        view = UserModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_admin(self):
        factory = APIRequestFactory()
        request = factory.post(self.url, {'username': 'test_user_x', 'password': 'qazwsx123',
                                          'email': 'mail222@mail.ru'}, format='json')
        admin = User.objects.create_superuser('admin3', 'admin3@mail.ru', 'qazwsx')  # создадим администратора
        force_authenticate(request, admin)
        view = UserModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detail(self):
        client = APIClient()  # клиент для удобной отправки REST-запросов (используется наиболее часто)
        # Создать user через ORM для проверки детализации
        user = User.objects.create(username='test_user', email='test@mail.ru', password='qazwsx')
        response = client.get(f'{self.url}{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_guest(self):
        client = APIClient()
        user = User.objects.create(username='test_user', email='test@mail.ru', password='qazwsx')
        response = client.put(f'{self.url}{user.id}/', username='test_user2', email='test2@mail.ru', password='qazwsx')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_admin(self):
        client = APIClient()
        user = User.objects.create(username='test_user1', email='test1@mail.ru', password='qazwsx')
        admin = User.objects.create_superuser('admin', 'admin2@mail.ru', 'qazwsx')  # создадим администратора
        client.login(username='admin', password='qazwsx')  # логинимся
        response = client.put(f'{self.url}{user.id}/',
                              {'username': 'test_user2', 'email': 'test2@mail.ru', 'password': 'qazwsx'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=user.id)  # Делаем проверку на произведение изменений
        self.assertEqual(user.username, 'test_user2')
        self.assertEqual(user.email, 'test2@mail.ru')
        client.logout()  # разлогинимся

    # Очистка после тестов
    def tearDown(self) -> None:
        pass


class TestMath(APISimpleTestCase):
    # APISimpleTestCase для тестирования, не связанного с базой данных
    # (применяется очень редко, удобен для тестирования внутренних функций)
    def test_sqrt(self):
        import math
        self.assertEqual(math.sqrt(4), 2)


