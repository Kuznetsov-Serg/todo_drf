from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, StringRelatedField
from users.serializers import UserModelSerializer
from .models import Project, Todo


class ProjectModelSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        # exclude = ('users',)

# Дополнительный серелизатор - будем его вызывать только для GET-запросов (views)
class ProjectModelSerializerExt(ModelSerializer):
    # users = StringRelatedField(many=True)       # не даст редактировать список, но показывает прикольно
    # users = UserModelSerializer(many=True)      # Та-же ерунда
    class Meta:
        model = Project
        fields = '__all__'
        # exclude = ('users',)

class TodoModelSerializer(ModelSerializer):
    # user = UserModelSerializer()
    class Meta:
        model = Todo
        fields = '__all__'
        # read_only_fields = ('is_active',)


class TodoModelSerializerV2(ModelSerializer):
    class Meta:
        model = Todo
        exclude = ('created', 'updated', )