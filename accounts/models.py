from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from product.models import Product, Variation

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, related_name="address", on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=False, verbose_name="Nome")
    address = models.CharField(max_length=120, blank=False, verbose_name="Endereço")
    complement = models.CharField(max_length=100, blank=True)
    neighborhood = models.CharField(max_length=50, blank=False)
    number = models.CharField(max_length=10, blank=False)
    tel = PhoneNumberField(blank=False, null=False)
    city = models.CharField(max_length=40, blank=False, null=False)
    cep = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False)
    
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        constraints = [ models.UniqueConstraint(fields=["user", "name"], name="unique_address_name_per_user")]
        indexes = [ models.Index(fields=["user"]), models.Index(fields=["cep"])]
    
    
    def __str__(self):
        return f"{self.user} - {self.user.username}"
    
class Inventory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="inventory")
    
    def __str__(self):
        return f"Inventory of {self.user.username}"
    
class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} X {self.quantity}"