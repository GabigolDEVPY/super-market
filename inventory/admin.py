from django.contrib import admin
from . models import Inventory, InventoryItem



# Register your models here.
@admin.register(Inventory)
class Inventory(admin.ModelAdmin):
    list_display = ("user",)
    
@admin.register(InventoryItem)
class Inventory(admin.ModelAdmin):
    list_display = ("inventory", "product", "quantity", "added_at")