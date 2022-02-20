from django.contrib import admin
from .models import Cart, OffCode, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 2


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'final_price',)
    search_fields = ('customer',)
    list_filter = ('created',)
    raw_id_fields = ('customer', 'off_code')
    inlines = (CartItemInline,)


@admin.register(OffCode)
class OffCodeAdmin(admin.ModelAdmin):
    list_display = ('value', 'type',)
    search_fields = ('value', 'type')
    list_filter = ('created',)
    exclude = ('delete_timestamp', 'deleted_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'count',)
    search_fields = ('product',)
    list_filter = ('cart',)
    raw_id_fields = ('cart', 'product')
