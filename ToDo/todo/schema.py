import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from projects.models import Project, Todo
from users.models import User

# level 1
# Пример из документации
# class Query(ObjectType):
#     # определяем поле hello без аргументов
#     hello = graphene.String(default_value="Hi!")
#
# schema = graphene.Schema(query=Query)

# level 2
# class ProjectType(DjangoObjectType):
#     class Meta:
#         model = Project
#         fields = '__all__'
#
#
# class Query(ObjectType):
#     all_projects = graphene.List(ProjectType)
#
#     def resolve_all_projects(root, info):
#         return Project.objects.all()
#
#
# schema = graphene.Schema(query=Query)


# level 3
# class ProjectType(DjangoObjectType):
#     class Meta:
#         model = Project
#         fields = '__all__'
#
#
# class TodoType(DjangoObjectType):
#     class Meta:
#         model = Todo
#         fields = '__all__'
#
#
# class Query(ObjectType):
#     all_projects = graphene.List(ProjectType)
#     all_todo = graphene.List(TodoType)
#
#     def resolve_all_projects(root, info):
#         return Project.objects.all()
#
#     def resolve_all_todo(root, info):
#         return Todo.objects.all()
#
#
# schema = graphene.Schema(query=Query)


# # level 4 (Запрос с параметром)
# class ProjectType(DjangoObjectType):
#     class Meta:
#         model = Project
#         fields = '__all__'
#
#
# class TodoType(DjangoObjectType):
#     class Meta:
#         model = Todo
#         fields = '__all__'
#
#
# class UserType(DjangoObjectType):
#     class Meta:
#         model = User
#         fields = '__all__'
#
#
# class Query(ObjectType):
#     # project_by_id = graphene.Field(ProjectType, id=graphene.Int(required=True))
#     project_by_id = graphene.Field(ProjectType, id=graphene.Int(required=False))
#     user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))
#     todo_by_user_name = graphene.List(TodoType, first_name=graphene.String(required=False))
#
#     def resolve_project_by_id(root, info, id=None):
#         if id:
#             try:
#                 return Project.objects.get(id=id)
#             except Project.DoesNotExist:
#                 return None
#         return Project.objects.all()
#
#     def resolve_user_by_id(root, info, id=None):
#         if id:
#             try:
#                 return User.objects.get(id=id)
#             except User.DoesNotExist:
#                 return None
#         return User.objects.all()
#
#     def resolve_todo_by_user_name(self, info, first_name=None):
#         todo = Todo.objects.all()
#         if first_name:
#             todo = todo.filter(user__first_name=first_name)
#         return todo
#
#
# schema = graphene.Schema(query=Query)


# level 5 (Изменения)
class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = '__all__'


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class Query(ObjectType):
    project_by_id = graphene.Field(ProjectType, id=graphene.Int(required=True))
    user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))
    todo_by_user_name = graphene.List(TodoType, first_name=graphene.String(required=False))

    def resolve_project_by_id(root, info, id=None):
        if id:
            try:
                return Project.objects.get(id=id)
            except Project.DoesNotExist:
                return None
        return Project.objects.all()

    def resolve_user_by_id(root, info, id=None):
        if id:
            try:
                return User.objects.get(id=id)
            except User.DoesNotExist:
                return None
        return User.objects.all()

    def resolve_todo_by_user_name(self, info, first_name=None):
        todo = Todo.objects.all()
        if first_name:
            todo = todo.filter(user__first_name=first_name)
        return todo

# Любое изменение - это мутация
class ProjectUpdateMutation(graphene.Mutation):
    # Класс для передачи параметров
    class Arguments:
        name = graphene.String(required=True)
        id = graphene.ID()

    # project будет содержать итоговый объект после изменения
    project = graphene.Field(ProjectType)

    # Логика изменения
    @classmethod
    def mutate(cls, root, info, name, id):
        project = Project.objects.get(id=id)
        project.name = name
        project.save()
        # Возвращаем объект мутации
        return ProjectUpdateMutation(project=project)


class ProjectCreateMutation(graphene.Mutation):
    # Класс для передачи параметров
    class Arguments:
        name = graphene.String()
        repository_url = graphene.String()
        # Mutation.createProject(users:) argument type must be Input Type but got: [UserType]!.
        # users = graphene.List(UserType, required=True)  # не понятно, как объявить, чтобы создать со списком пользователей

    # project будет содержать итоговый объект после изменения
    project = graphene.Field(ProjectType)

    # Логика изменения
    @classmethod
    def mutate(cls, root, info, name, repository_url):
        project = Project(name=name, repository_url=repository_url)
        project.save()
        # Возвращаем объект мутации
        return ProjectCreateMutation(project=project)


class ProjectDeleteMutation(graphene.Mutation):
    # Класс для передачи параметров
    class Arguments:
        id = graphene.ID(required=True)

    # project будет содержать итоговый объект после изменения
    project = graphene.Field(ProjectType)

    # Логика изменения
    @classmethod
    def mutate(cls, root, info, id):
        project = Project.objects.get(id=id).delete()
        # Возвращаем объект мутации
        return ProjectDeleteMutation(project=project)


# Класс для всех мутаций
class Mutation(ObjectType):
    create_project = ProjectCreateMutation.Field()
    update_project = ProjectUpdateMutation.Field()
    delete_project = ProjectDeleteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

# mutation updateProject {
#     updateProject(id: 5, name: "Проект с новым именем") {
#     project {
#     id
# name
# repositoryUrl
# users {
#     username
# }
# }
# }
# }

# mutation createProject {
#     createProject(name: "Личный сайт студента", repositoryUrl: "http://e99920zb.beget.tech/index.php") {
#     project {
#     id
# name
# repositoryUrl
# users {
#     id
# username
# }
# }
# }
# }

# mutation ProjectDelete{
#     deleteProject(id: 16) {
#     project{
#     name
# repositoryUrl
# }
# }
# }

# Для работы через запросы "Qery"
# http://127.0.0.1:8000/graphql_no_graph/?query={projectById(id:6){name%20repositoryUrl%20users{username}}}