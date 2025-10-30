from django.db import models
import string
import random
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Products


class Inventory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="inventory")
    
    def __str__(self):
        return f"Inventory of {self.user.username}"
    
class InventoryItem(models.Model):
    inventory = models.ForeignKey("Inventory", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} X {self.quantity}"
    