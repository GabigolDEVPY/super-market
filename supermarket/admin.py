from django.contrib import admin
from .models import Banners, Photos

@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    list_display = ("name",)
    
@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    list_display = ("id",)