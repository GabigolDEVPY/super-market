from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from PIL import Image
from django.conf import settings
import os
from django.contrib.auth.models import User
from django.forms import CharField
from django.utils import timezone


class Photos(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='photos/')
    icon = models.ImageField(upload_to='photos/')
    
    def __str__(self):
        return self.name

class Banners(models.Model):
    name = models.CharField(max_length=40)
    banner = models.ImageField(upload_to='banners/')
    
    def __str__(self):
        return self.name