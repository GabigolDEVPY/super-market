from django.contrib import admin
from . models import Cart, CartItem, Payment_Code

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at") 
    

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")
    
    
@admin.register(Payment_Code)
class PaymentCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at", "is_paid")