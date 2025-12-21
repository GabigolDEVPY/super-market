from django.shortcuts import render, redirect
from product.models import Product, Category
from django.views.generic import ListView

class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.prefetch_related("products").all()
        context["user"] = self.request.user 
        return context
    
class AllProducts(ListView):
    model = Product
    template_name = "allproducts.html"
    context_object_name = "products"
    paginate_by = 6
    ordering = ["id"]
    
    


    