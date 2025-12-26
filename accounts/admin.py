from django.contrib import admin
from .models import Address, Inventory


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("name","user")
    
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("user",)