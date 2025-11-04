from django.shortcuts import render, redirect
from product.models import Product
from django.views.generic import ListView

class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"
    
    def get_queryset(self):
        return Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user 
        return context
    



    