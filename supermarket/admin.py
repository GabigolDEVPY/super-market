from django.contrib import admin
from .models import Banners, Principal, Footer

@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    list_display = ("name",)
    
@admin.register(Principal)
class PrincipalAdmin(admin.ModelAdmin):
    list_display = ("name_shop",)
    
@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ("id",)