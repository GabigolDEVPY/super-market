from . models import Cart, Inventory
from django.contrib.auth.models import User
from django.dispatch import receiver

from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_cart_and_inventory(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
        Inventory.objects.create(user=instance)