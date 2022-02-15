from django.contrib import admin
from .models import Customer, Address


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',)
    search_fields = ('username', 'email',)
    inlines = [AddressInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('state', 'city', 'customer')
    search_fields = ('state', 'city', 'customer')
    list_filter = ('last_updated',)
