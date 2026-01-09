from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from product.models import Product

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

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=30 ,default="Pendente", choices=(
        ('A', 'Aprovado'),
        ('P', 'Pendente'),
        ('R', 'Reprovado'),
        ('E', 'Enviado'),
        ('A', 'Finalizado')
    ))
    address = models.ForeignKey(InfosForm, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"Pedido N. {self.pk}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Item do pedido N. {self.order}"    