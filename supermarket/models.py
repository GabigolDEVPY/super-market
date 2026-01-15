from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from PIL import Image
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
import os
from django.contrib.auth.models import User
from django.forms import CharField
from django.utils import timezone

class Footer(models.Model):
    link_1 = models.CharField(max_length=60)
    link_2 = models.CharField(max_length=60)
    link_3 = models.CharField(max_length=60)
    email = models.EmailField(blank=False, null=False)
    contact = PhoneNumberField(blank=False, null=False)
    whatsapp = PhoneNumberField(blank=False, null=False)
    short_description = models.CharField(max_length=200)

class Pricipal(models.Model):
    name_shop = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='photos/')
    icon = models.ImageField(upload_to='photos/')
    
    def __str__(self):
        return self.name

class Banners(models.Model):
    name = models.CharField(max_length=40)
    banner = models.ImageField(upload_to='banners/')
    
    def __str__(self):
        return self.name