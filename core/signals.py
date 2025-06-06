from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from .models import OrderItem

@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    total = Decimal('0.00')
    for item in order.items.all():
        total += item.product.price * item.quantity
    order.total = total
    order.save()
