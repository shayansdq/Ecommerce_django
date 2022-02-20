from django.contrib import admin
from .models import Customer, Address
from django.contrib.auth.admin import UserAdmin
from core.models import User

UserAdmin.list_display = ('phone', 'email', 'first_name', 'last_name', 'is_staff')
UserAdmin.search_fields = ('phone', 'first_name', 'last_name', 'email')
UserAdmin.ordering = ('phone',)
UserAdmin.fieldsets[0][1]['fields'] = ('phone', 'password')
UserAdmin.add_fieldsets[0][1]['fields'] = ('phone', 'password1','password2')

admin.site.register(User, UserAdmin)


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender',)
    search_fields = ('user', 'gender',)
    inlines = [AddressInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('state', 'city', 'customer')
    search_fields = ('state', 'city', 'customer')
    list_filter = ('last_updated',)
