from django.db import models
from django.contrib.auth.models import User
from product.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"

    def __str__(self):
        return f"Carrinho de {self.user.username}"
    
    @property
    def total_price(self):
        return sum(item.product.apply_discount() * item.quantity for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = 'Item Carrinho'
        verbose_name_plural = 'Itens Carrinhos'
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
        




