from django.contrib import admin

from .models import User

# admin.site.register(ShopUser)
@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "password")
    list_filter = ('is_active', 'is_staff', 'is_superuser')

# admin.site.register(User)
