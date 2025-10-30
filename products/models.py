from django.db import models
import string
import random
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=60, null=True, blank=True)
    
    def __str__(self):
        return self.category

class Products(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Stock(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} unidades"
    
