from django.contrib import admin

from apps.blog.models import Tag
from apps.catalog.models import Category, Product, ProductImage


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


class ProductCategoryInline(admin.TabularInline):
    model = Product.categories.through
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ['product', 'image_tag', 'image', 'is_main']
    readonly_fields = ['image_tag']
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    inlines = [ProductCategoryInline, ProductImageInline]
    list_display = ['id', 'image_tag', 'name', 'quantity', 'price', 'is_checked','user', 'created_at']
    list_display_links = ['id', 'name', 'image_tag']
