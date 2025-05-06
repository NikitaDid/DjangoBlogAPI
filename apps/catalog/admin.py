from django.contrib import admin

from apps.blog.models import Tag
from apps.catalog.models import Category, Product


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


class ProductCategoryInline(admin.TabularInline):
    model = Product.categories.through
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    inlines = [ProductCategoryInline]