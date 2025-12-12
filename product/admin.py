from csv import list_dialects
from django.contrib import admin
from . models import Product, Stock, Category, Promotion, DiscountCode, ImagesProduct, Variation




@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "updated_at")
    
@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ("category",)    
    
@admin.register(Promotion)
class Promotion(admin.ModelAdmin):
    list_display = ("name",)
    
@admin.register(DiscountCode)
class DiscountCode(admin.ModelAdmin):
    list_display = ("name",)
    
@admin.register(ImagesProduct)
class ImagesProduct(admin.ModelAdmin):
    list_display = ("name",)
    

class VariationAdmin(admin.TabularInline):
    model = Variation
    extra = 1
    
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_date")
    inlines = [
        VariationAdmin
    ]
