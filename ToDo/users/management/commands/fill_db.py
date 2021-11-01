from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404


import json
import os

from users.models import User

from openpyxl import Workbook   # для работы с Excel
import pandas as pd             # для работы с Excel

# from django.core.exceptions import DoesNotExist     # для обработки исключения


JSON_PATH = 'users/import'
EXCEL_PATH = 'users/import'

class Command(BaseCommand):
    def handle(self, *args, **options):
        convert_EXCEL_file_to_JSON_file('users')    # Конвертируем из excel (легче набивать) в JSON
        users = load_from_json('users')

        User.objects.all().delete()     # Удалим все записи из БД
        for user in users:
            # new_user = User(username=user['username'],
            #                 first_name=user['first_name'],
            #                 last_name=user['last_name'],
            #                 email=user['email'],
            #                 password=user['password'],
            #                 )
            new_user = User(**user)
            new_user.set_password(user['password'])     # для хэширования пароля
            new_user.save()

        # Создаем суперпользователя при помощи менеджера модели
        # user = get_object_or_404(User, username='kuznetsov')
        # user.delete()
        User.objects.create_superuser('kuznetsov', 'ksn1974@mail.ru', '1')

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


# Конвертируем перечень товаров из excel в JSON
def convert_EXCEL_file_to_JSON_file (file_name):
    # data = pd.read_excel(path, usecols="A,E:F", encoding='utf8')
    data = pd.read_excel(os.path.join(EXCEL_PATH, file_name + '.xlsx'))
    # i = path.find('.', len(path)-6)     # избавимся от расширения
    # path_JSON = path[:i]+'.json'         # установим расширение файла для сохранения
    path_JSON = os.path.join(JSON_PATH, file_name + '.json')
    data.to_json(path_or_buf=path_JSON, orient='records')
    return path_JSON

# считаем JSON из файла
def read_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)
    # return json.loads(read_file(file_name_with_path))




