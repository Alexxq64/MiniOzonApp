# core/models.py
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories', 
        verbose_name='Родительская категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    class MPTTMeta:
        order_insertion_by = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

class Role(models.TextChoices):
    BUYER = 'buyer', _('Покупатель')
    SELLER = 'seller', _('Продавец')

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)

    def __str__(self):
        return f"{self.username} ({self.role})"
