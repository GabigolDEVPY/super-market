from django.contrib import admin
from . models import Product, Stock, Category, Promotion


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_date")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "updated_at")
    
@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ("category",)    
    
@admin.register(Promotion)
class Promotion(admin.ModelAdmin):
    list_display = ("name",)