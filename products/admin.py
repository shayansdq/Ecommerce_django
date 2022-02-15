from django.contrib import admin
from .models import Product, Brand, Category, Discount


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name', 'category', 'brand')
    list_filter = ('inventory',)
    raw_id_fields = ('brand', 'discount', 'category')
    fieldsets = (
        ('information',
         {'fields': ['name', 'price', 'description', 'brand', 'category']}),
        ('Specifications',
         {'fields': ['discount', 'inventory', 'slug', 'picture']})
    )
    prepopulated_fields = {'slug': ('description',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_display_links = ('name',)
    search_fields = ('name', 'country')
    list_filter = ('name', 'country')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('value', 'type')
    search_fields = ('value',)
