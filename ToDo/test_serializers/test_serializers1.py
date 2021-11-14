import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from test_models import Author


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    birthday_year = serializers.IntegerField()

    def create(self, validated_data):
        return Author(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.birthday_year = validated_data.get('birthday_year', instance.birthday_year)
        return instance

    def validate_birthday_year(self, value):
        if value < 0:
            raise serializer.ValidationError('Год рождения не может быть отрицательным')
        return value

    def validate(self, attrs):      # для валидации нескольких полей
        if 'name' not in attrs: return attrs    # для исключения ошибки при вызове частичного обновления (поле не передается)
        if attrs['name'] == 'Толстой' and attrs['birthday_year'] != 1828:
            raise serializers.ValidationError('Неверный год рождения Толстого')
        return attrs



author = Author('Пушкин', 1880)
serializer = AuthorSerializer(author)

renderer = JSONRenderer()
json_bytes = renderer.render(serializer.data)

stream = io.BytesIO(json_bytes)
data = JSONParser().parse(stream)

# data = {'name': 'Пушкин', 'birthday_year': 1880}
# serializer = AuthorSerializer(author, data=data)
serializer = AuthorSerializer(data=data)
serializer.is_valid()

author = serializer.save()      # если serializer.is_valid() = False, не обновит
print(type(author))
print(author, author.birthday_year)

data = {'name': 'Толстой', 'birthday_year': 1828}
serializer = AuthorSerializer(author, data=data)    # пытаемся обновить (отправляем instance)
serializer.is_valid()                   # есл у Толстой не проходит год рождения 1828 (ошибка)
author = serializer.save()              # обновление не пройдет
print('Заменим instance')
print(author, author.birthday_year)
#
data = {'birthday_year': 2000}
serializer = AuthorSerializer(author, data=data, partial=True)
serializer.is_valid()
author = serializer.save()
print('Попытка частичной замены instance')
print(author, author.birthday_year)

data = {'name': 'Герцен'}
serializer = AuthorSerializer(author, data=data, partial=True)
serializer.is_valid()
author = serializer.save()
print('Успешная попытка частичной замены instance')
print(author, author.birthday_year)

data = {'birthday_year': 2000}
serializer = AuthorSerializer(author, data=data, partial=True)
serializer.is_valid()
author = serializer.save()
print('Попытка частичной замены instance')
print(author, author.birthday_year)

data = {'name': 'Толстой', 'birthday_year': 2000}
serializer = AuthorSerializer(author, data=data)

if serializer.is_valid():
    author = serializer.save()
    print(author, author.birthday_year)
else:
    print(serializer.errors)

# data = {'name': 'Толстой', 'birthday_year': 1828}
# serializer = AuthorSerializer(data=data)    # пытаемся обновить (отправляем instance)
# serializer.is_valid()                   # есл у Толстой не проходит год рождения 1828 (ошибка)
# author = serializer.save()              # обновление не пройдет
# print(author, author.birthday_year)
#
# data = {'birthday_year': 2000}
# serializer = AuthorSerializer(author, data=data, partial=True)
# if serializer.is_valid():
#     author = serializer.save()
#     print(author, author.birthday_year)
# else:
#     print(serializer.errors)