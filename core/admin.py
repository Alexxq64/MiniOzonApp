# core/admin.py
from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']  # Показываем имя и родительскую категорию
    list_filter = ['parent']  # Фильтруем по родительским категориям
    search_fields = ['name']  # Возможность поиска по имени

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']  # Показываем имя, категорию и цену
    list_filter = ['category']  # Фильтруем по категориям
    search_fields = ['name']  # Возможность поиска по имени

admin.site.register(Category, CategoryAdmin)  # Регистрируем модель Category
admin.site.register(Product, ProductAdmin)    # Регистрируем модель Product
