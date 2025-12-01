from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, related_name="infos", on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=120, blank=False)
    complement = models.CharField(max_length=100, blank=True)
    neighborhood = models.CharField(max_length=50, blank=False)
    number = models.CharField(max_length=10)
    tel = PhoneNumberField(blank=False, null=False)
    city = models.CharField(max_length=40, blank=False, null=False)
    cep = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False)
    
    
    