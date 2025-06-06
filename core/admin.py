from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

from .models import (
    Category, Product, User,
    Cart, CartItem,
    Order, OrderItem,
    OrderStatus
)

# --- Category ---
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)
    ordering = ['parent']
    list_display_links = ('name',)

# --- Product ---
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name',)

# --- User ---
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Роль и права', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

# --- Cart ---
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity')
    can_delete = False

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    inlines = [CartItemInline]

# --- Order ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity')
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    change_form_template = 'admin/core/order/change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/mark-<str:status>/', self.admin_site.admin_view(self.mark_status), name='order-mark-status'),
        ]
        return custom_urls + urls

    def mark_status(self, request, order_id, status):
        order = self.get_object(request, order_id)
        if not order:
            self.message_user(request, "Заказ не найден.", level=messages.ERROR)
            return redirect("..")

        if status not in OrderStatus.values:
            self.message_user(request, f"Недопустимый статус: {status}", level=messages.ERROR)
        else:
            order.status = status
            order.save()
            self.message_user(request, f"Статус заказа №{order.id} обновлён на «{OrderStatus(status).label}».", level=messages.SUCCESS)

        return redirect(f"../../{order_id}/change/")

# --- Admins for items (optional) ---
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__name')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__user__username', 'product__name')

# --- Register Models ---
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
