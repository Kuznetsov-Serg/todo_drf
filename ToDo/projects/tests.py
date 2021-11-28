from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APISimpleTestCase, APITestCase
from mixer.backend.django import mixer
from django.contrib.auth.models import User

from .views import ProjectModelViewSet, TodoModelViewSet
from .models import Project, Todo
from users.models import User


class TestProjectViewSet(TestCase):
    url = '/api/projects/'
    password = 'qazwsx123'

    # admin = None

    # Подготовка к тестам (данные,...)
    # Повторяющийся код тестов можно вынести в метод setUp
    def setUp(self) -> None:
        # self.client = APIClient()
        self.admin = User.objects.create_superuser('admin', 'admin@mail.ru', self.password)  # создадим администратора
        # self.client.force_authenticate(user=self.admin)

    def test_get_list_project(self):
        # APIRequestFactory (фабрика для создания запросов, используется редко) - для изолированной проверки View
        # (не учитывает URL и на делает реальных запросов)
        factory = APIRequestFactory()  # создать объект класса
        request = factory.get(self.url)  # определяем адрес и метод отправки запроса
        # указываем тип запроса для ModelViewSet и способ (create, destroy, list, update)
        view = ProjectModelViewSet.as_view({'get': 'list'})
        response = view(request)  # передаем во view и получаем ответ
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project_by_guest(self):
        factory = APIRequestFactory()
        request = factory.post(self.url, {'name': 'Тестовый проект', 'repository_url': 'https://github.com/',
                                          'users': [self.admin.id]})
        view = ProjectModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project_by_admin(self):
        factory = APIRequestFactory()
        request = factory.post(self.url, {'name': 'Тестовый проект', 'repository_url': 'https://github.com/',
                                          'users': [self.admin.id]})
        force_authenticate(request, self.admin)
        view = ProjectModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detail(self):
        client = APIClient()  # клиент для удобной отправки REST-запросов (используется наиболее часто)
        # Создать user через ORM для проверки детализации
        project = Project.objects.create(name='Тестовый проект', repository_url='https://github.com/')
        # (users - непустой список) direct assignment to the forward side of a many-to-many set is prohibited - > use set instead
        project.users.add(self.admin.id)
        project.save()
        response = client.get(f'{self.url}{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_guest(self):
        client = APIClient()
        project = Project.objects.create(name='Тестовый проект', repository_url='https://github.com/')
        project.users.add(self.admin.id)
        project.save()
        response = client.put(f'{self.url}{project.id}/', name='Тестовый проект2', repository_url='https://yandex.ru/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_admin(self):
        client = APIClient()
        project = Project.objects.create(name='Тестовый проект', repository_url='https://github.com/')
        project.users.add(self.admin.id)
        project.save()
        client.login(username=self.admin.username, password=self.password)  # логинимся
        response = client.put(f'{self.url}{project.id}/',
                              {'name': 'Тестовый проект2', 'repository_url': 'https://yandex.ru/',
                               'users': [self.admin.id]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project = Project.objects.get(id=project.id)  # Делаем проверку на произведение изменений
        self.assertEqual(project.name, 'Тестовый проект2')
        self.assertEqual(project.repository_url, 'https://yandex.ru/')
        client.logout()  # разлогинимся

    # Очистка после тестов
    def tearDown(self) -> None:
        pass


class TestTodoViewSet(APITestCase):
    url = '/api/todo/'
    password = 'qazwsx123'

    # Подготовка к тестам (данные,...)
    # Повторяющийся код тестов можно вынести в метод setUp
    # Установки запускаются перед каждым тестом
    def setUp(self) -> None:
        self.admin = User.objects.create_superuser('admin', 'admin@mail.ru', self.password)  # создадим администратора

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_admin(self):
        project = Project.objects.create(name='Тестовый проект', repository_url='https://github.com/')
        # project.users.add(self.admin.id)
        # project.save()
        todo = Todo.objects.create(title='Тестовая заметка', text='Это описание тестовой заметки', project=project,
                                   user=self.admin)
        self.client.login(username=self.admin.username, password=self.password)  # логинимся
        response = self.client.put(f'{self.url}{todo.id}/',
                                   {'title': 'Тестовая заметка 2', 'text': 'Это описание тестовой заметки 2',
                                    'project': project.id, 'user': self.admin.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo = Todo.objects.get(id=todo.id)  # Делаем проверку на произведение изменений
        self.assertEqual(todo.title, 'Тестовая заметка 2')
        self.assertEqual(todo.text, 'Это описание тестовой заметки 2')
        self.client.logout()  # разлогинимся

    def test_edit_admin_with_mixer(self):   # Для быстрой генерации тестовых данных
        # project = mixer.blend(Project)      # Создает элементы БД и сама заботится о создании связанных сущностей!!
        project = mixer.blend(Project, name='Тестовый проект')  # Можем подменять рандомные данные полей
        todo = Todo.objects.create(title='Тестовая заметка', text='Это описание тестовой заметки', project=project,
                                   user=self.admin)
        self.client.login(username=self.admin.username, password=self.password)  # логинимся
        response = self.client.put(f'{self.url}{todo.id}/',
                                   {'title': 'Тестовая заметка 2', 'text': 'Это описание тестовой заметки 2',
                                    'project': project.id, 'user': self.admin.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo = Todo.objects.get(id=todo.id)  # Делаем проверку на произведение изменений
        self.assertEqual(todo.title, 'Тестовая заметка 2')
        self.assertEqual(todo.text, 'Это описание тестовой заметки 2')
        self.assertEqual(project.name, 'Тестовый проект')
        self.client.logout()  # разлогинимся

# class TestMath(APISimpleTestCase):
#     # APISimpleTestCase для тестирования, не связанного с базой данных
#     # (применяется очень редко, удобен для тестирования внутренних функций)
#     def test_sqrt(self):
#         import math
#         self.assertEqual(math.sqrt(4), 2)
