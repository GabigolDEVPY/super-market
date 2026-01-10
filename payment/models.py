from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from stripe import Balance
from product.models import Product, Variation

# Create your models here.
class InfosForm(models.Model):
    user = models.ForeignKey(User, related_name="address_order", on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=120, blank=False)
    complement = models.CharField(max_length=100, blank=True)
    neighborhood = models.CharField(max_length=50, blank=False)
    number = models.CharField(max_length=10)
    tel = PhoneNumberField(blank=False, null=False)
    city = models.CharField(max_length=40, blank=False, null=False)
    cep = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False)
    
    def __str__(self):
        return str(self.address)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=30 ,default="P", choices=(
        ('A', 'Aprovado'),
        ('P', 'Pendente'),
        ('R', 'Reprovado'),
        ('E', 'Enviado'),
        ('F', 'Finalizado'),
    ))
    address = models.ForeignKey(InfosForm, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"Pedido N. {self.pk}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False)
    variant = models.ForeignKey(Variation, on_delete=models.CASCADE, blank=True, null=False)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    
    def __str__(self):
        return f"Item do pedido N. {self.order}"    