from django.db import models
import string
import random
from django.contrib.auth.models import User
from django.utils import timezone
import product
from product.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Carrinho de {self.user.username}"
    
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    @property
    def subtotal(self):
        return (self.product.price - (self.product.price * self.product.discount.discount / 100))  if self.product.discount else self.product.price * self.quantity

def generate_payment_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

class Payment_Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_codes")
    code = models.CharField(max_length=15, unique=True, default=generate_payment_code)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        status = "Pago" if self.is_paid else "Pendente"
        return f"{self.user.username} - {self.code} ({status})"