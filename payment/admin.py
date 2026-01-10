from django.contrib import admin
from . models import InfosForm, Order, OrderItem


@admin.register(InfosForm)
class InfosForm(admin.ModelAdmin):
    list_display = ("user",) 
    
class OrderItem(admin.TabularInline):
    model = OrderItem
    extra = 1
    

@admin.register(Order)
class Order(admin.ModelAdmin):
    inlines = [
        OrderItem
    ]
    list_display = ("pk", "price", "status", "user", "order_create_time", "order_update_time") 
