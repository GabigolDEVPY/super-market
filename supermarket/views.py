from django.shortcuts import render, redirect
from product.models import Product, Category
from django.db.models import Q
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
    paginate_by = 3
    ordering = ["id"]

class SearchProduct(AllProducts):
    def get_queryset(self, *args, **kwargs):
        search_parameter = self.request.GET.get("parameter")
        if not search_parameter:
            return redirect("home")
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            Q(name__icontains=search_parameter) |
            Q(price__icontains=search_parameter) |
            Q(description__icontains=search_parameter) 
            )
        return query_set


    