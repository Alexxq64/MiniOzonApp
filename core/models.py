# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

# Категории с иерархией
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

# Продукты
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

# Роли пользователей
class Role(models.TextChoices):
    BUYER = 'buyer', _('Покупатель')
    SELLER = 'seller', _('Продавец')
    ADMIN = 'admin', _('Администратор')

# Пользователь
class User(AbstractUser):
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)

    def __str__(self):
        return f"{self.username} ({self.role})"

# Корзина (одна на пользователя)
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

# Элемент корзины
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

# Статусы заказа
class OrderStatus(models.TextChoices):
    PENDING = 'pending', _('В ожидании')
    PROCESSING = 'processing', _('В обработке')
    COMPLETED = 'completed', _('Завершён')
    CANCELED = 'canceled', _('Отменён')

# Заказ
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма')
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name='Статус'
    )

    def __str__(self):
        return f"Заказ #{self.pk} от {self.user.username}"

    def update_total(self):
        total = sum(item.product.price * item.quantity for item in self.items.all())
        self.total = total
        self.save(update_fields=['total'])

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

# Элемент заказа
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
