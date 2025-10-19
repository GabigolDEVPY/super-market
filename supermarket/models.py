from itertools import product
from django.db import models
from django.utils import timezone

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    Created_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
    
class Stock(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} unidades"