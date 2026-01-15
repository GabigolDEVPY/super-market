from django.contrib import admin
from .models import Banners, Pricipal

@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    list_display = ("name",)
    
@admin.register(Pricipal)
class PrincipalAdmin(admin.ModelAdmin):
    list_display = ("id",)