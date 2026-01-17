from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Footer(models.Model):
    email = models.EmailField(blank=False, null=False)
    whatsapp = PhoneNumberField(blank=False, null=False)
    short_description = models.CharField(max_length=200)

class Principal(models.Model):
    name_shop = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='photos/')
    icon = models.ImageField(upload_to='photos/')
    
    def __str__(self):
        return self.name

class Banners(models.Model):
    name = models.CharField(max_length=40)
    banner = models.ImageField(upload_to='banners/')
    banner_mobile = models.ImageField(upload_to='banners/')
    
    def __str__(self):
        return self.name