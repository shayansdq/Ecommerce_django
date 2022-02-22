from django.contrib.auth.admin import UserAdmin
from core.models import User
from django.contrib import admin


UserAdmin.list_display = ('phone', 'email', 'first_name', 'last_name', 'is_staff')
UserAdmin.search_fields = ('phone', 'first_name', 'last_name', 'email')
UserAdmin.list_display = ('username', 'phone', 'last_name', 'email')
UserAdmin.ordering = ('phone',)
UserAdmin.fieldsets[0][1]['fields'] = ('phone', 'username','password')
UserAdmin.add_fieldsets[0][1]['fields'] = ('phone', 'username', 'password1', 'password2')
UserAdmin.prepopulated_fields = {'username': ('phone',)}
admin.site.register(User, UserAdmin)
