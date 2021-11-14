from django.contrib import admin

from .models import User

# admin.site.register(User)
@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", )
    list_filter = ('is_active', 'is_staff', 'is_superuser')
