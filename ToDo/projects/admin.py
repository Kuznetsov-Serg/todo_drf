from django.contrib import admin

from .models import Project, Todo


admin.site.register(Project)
# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    # list_filter = ('is_active', 'is_staff', 'is_superuser')

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    list_filter = ('is_active', 'project', 'user')
