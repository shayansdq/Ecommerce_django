from django.contrib import admin
from .models import Product, Brand, Category, Discount, Comment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name', 'category', 'brand')
    list_display_links = ('name',)
    list_per_page = 20
    list_filter = ('inventory',)
    raw_id_fields = ('brand', 'discount', 'category')
    fieldsets = (
        ('information',
         {'fields': ['name', 'price', 'description', 'brand', 'category']}),
        ('Specifications',
         {'fields': ['discount', 'inventory', 'slug', 'picture']})
    )
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('delete_timestamp', 'deleted_at', 'is_deleted', 'is_active')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_display_links = ('name',)
    list_per_page = 10
    search_fields = ('name', 'country')
    list_filter = ('name', 'country')
    exclude = ('delete_timestamp', 'deleted_at', 'is_deleted', 'is_active')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'body')
    list_display_links = ('body',)
    list_per_page = 20
    search_fields = ('customer', 'body')
    list_filter = ('product',)
    raw_id_fields = ('reply',)
    exclude = ('delete_timestamp', 'deleted_at', 'is_deleted', 'is_active')


class ProductInline(admin.TabularInline):
    model = Product
    extra = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    inlines = (ProductInline,)
    exclude = ('delete_timestamp', 'deleted_at', 'is_deleted', 'is_active')
    raw_id_fields = ('root',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('value', 'type')
    search_fields = ('value',)
    exclude = ('delete_timestamp', 'deleted_at', 'is_deleted', 'is_active')