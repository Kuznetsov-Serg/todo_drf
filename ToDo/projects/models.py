from django.db import models

from users.models import User


class Project(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='наименование',
    )
    repository_url = models.URLField(
        verbose_name='ссылка на репозиторий',
    )
    users = models.ManyToManyField(
        User,
        # on_delete=models.RESTRICT,
        verbose_name='пользователь',
    )

    def __str__(self):
        users = ', '.join([str(el) for el in User.objects.filter(project__id=self.pk)])
        return f'{self.name} ({users})'
        # return self.name

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'

class Todo(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name='проект',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        verbose_name='пользователь-создатель',
    )
    title = models.CharField(
        max_length=64,
        verbose_name='заголовок',
    )
    text = models.TextField(
        verbose_name='заметка',
    )
    is_active = models.BooleanField(
        verbose_name='активна',
        default=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} ({self.project.name}) - {self.user.first_name}'

    class Meta:
        verbose_name = 'заметка'
        verbose_name_plural = 'заметки'
