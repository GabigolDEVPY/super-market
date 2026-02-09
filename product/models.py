from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from PIL import Image
from django.conf import settings
import os
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=60, null=True, blank=True)
    
    def __str__(self):
        return self.category
    
    
class Promotion(models.Model):
    name = models.CharField(max_length=50, blank=False)
    discount = models.PositiveIntegerField(default=10)

    
    def __str__(self):
        return f"{self.name} ({self.discount}%)" 
    

class Product(models.Model):
    name = models.CharField(max_length=60)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="products")
    description = models.TextField()
    id_stripe = models.CharField(max_length=50, blank=True)
    discount = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_full = models.ImageField(upload_to='products/', null=True, blank=True)
    
    def has_stock(self):
        return self.variations.filter(stock__gt=0).exists()
    
    
    def resize_image(self, img, new_width):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)

        with Image.open(img_full_path) as img_pil:
            original_width, original_height = img_pil.size

            if original_width <= new_width:
                return
            new_height = round((new_width * original_height) / original_width)
            new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
            new_img.save(img_full_path, optimize=True, quality=50)
        
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        max_image_size = 800  
        
        if self.image:
            self.resize_image(self.image, max_image_size)
            
    def __str__(self):
        return self.name
    
    def apply_discount(self):
        if self.discount:
            discount_amount = (self.price * self.discount.discount) / Decimal("100")
            return (self.price - discount_amount).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        return (self.price).quantize(Decimal("0.00"))
    
    def twelvetimes(self):
        return (self.apply_discount() / 12).quantize(Decimal("0.00"))


class DiscountCode(models.Model):
    name = models.CharField(max_length=15, blank=False)
    discount = models.PositiveIntegerField()
    

    def __str__(self):
        return self.name

class ImagesProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    name = models.CharField(max_length=80)
    image = models.ImageField(upload_to="products/")
    
    def __str__(self):
        return f"{self.name}"
    
    
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variations")
    name = models.CharField(max_length=60)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    stock = models.PositiveBigIntegerField(default=0)
    
    def apply_discount(self):
        if self.product.discount:
            discount_amount = (self.price * self.product.discount.discount) / Decimal("100")
            return (self.price - discount_amount).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        return (self.price).quantize(Decimal("0.00"))
    

    def __str__(self):
        return self.name
    

        