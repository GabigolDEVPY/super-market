from django.contrib import admin
from .models import Product, Stock, Cart, CartItem, Payment_Code

@admin.register(Payment_Code)
class PaymentCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at", "is_paid")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_date")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "updated_at")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at") 
    

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")