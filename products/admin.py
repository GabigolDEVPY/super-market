from django.contrib import admin

# Register your models here.
@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_date")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "updated_at")
    
@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ("category",)    