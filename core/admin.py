# core/admin.py
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin  # Используем DraggableMPTTAdmin для отображения дерева категорий
from .models import Category, Product

class CategoryAdmin(DraggableMPTTAdmin):  # Используем DraggableMPTTAdmin вместо MPTTModelAdmin
    list_display = ('name', 'parent')  # Отображаем имя и родительскую категорию
    search_fields = ('name',)  # Возможность поиска по имени
    list_filter = ('parent',)  # Фильтруем по родительским категориям
    ordering = ['parent']  # Устанавливаем сортировку по родителю
    list_display_links = ('name',)  # Указываем, что поле 'name' будет ссылкой для редактирования

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')  # Показываем имя, категорию и цену
    list_filter = ('category',)  # Фильтруем по категориям
    search_fields = ('name',)  # Возможность поиска по имени

# Регистрируем модели в админке
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
