from django.contrib import admin
from core.models import User
from .models import Customer, Address, WishList, OtpCode


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender',)
    search_fields = ('user', 'gender',)
    inlines = (AddressInline,)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('state', 'city', 'customer')
    search_fields = ('state', 'city', 'customer')
    list_filter = ('last_updated',)


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product')
    search_fields = ('customer', 'product')
    list_filter = ('last_updated',)
    exclude = ('delete_timestamp', 'deleted_at', 'is_deleted', 'is_active')


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'created')
    search_fields = ('phone',)
    list_filter = ('created',)
