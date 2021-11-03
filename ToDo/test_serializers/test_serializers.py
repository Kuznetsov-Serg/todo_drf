import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from test_models import Author


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    birthday_year = serializers.IntegerField()


print(50*'*')
print('Serializer преобразует сложный объект в словарь, содержащий простые типы данных, а также выполняет обратное преобразование.\n')
author = Author('Грин', 1880)
serializer = AuthorSerializer(author)
print(serializer.data)  # {'name': 'Грин', 'birthday_year': 1880}
print(type(serializer.data))  # <class 'rest_framework.utils.serializer_helpers.ReturnDict'>

print(50*'*')
print('JSONRenderer - преобразовать его в независимый от языка python формат (набор байт, например JSON, HTML, XML…)\n')
renderer = JSONRenderer()
json_bytes = renderer.render(serializer.data)
print(json_bytes)  # b'{"name":"\xd0\x93\xd1\x80\xd0\xb8\xd0\xbd","birthday_year":1880}'
print(type(json_bytes))  # <class 'bytes'>

print(50*'*')
print('JSONParser - обратная Десериализация\n')
stream = io.BytesIO(json_bytes)
data = JSONParser().parse(stream)
print(stream)
print(data)  # {'name': 'Грин', 'birthday_year': 1880}
print(type(data))  # <class 'dict'>

print(50*'*')
serializer = AuthorSerializer(data=data)
print(serializer.is_valid())  # True - обязательно делать после каждого добавления данных в сериализатор, иначе ошибка!
print(serializer.validated_data)  # OrderedDict([('name', 'Грин'), ('birthday_year', 1880)])
print(type(serializer.validated_data))  # <class 'collections.OrderedDict'>
