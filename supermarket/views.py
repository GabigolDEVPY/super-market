from django.shortcuts import render, redirect
from products.models import Product

def home(request):
    user = request.user
    products = Product.objects.all()
    print(products)
    return render(request ,"home.html",
        context={
            "products": products
        })

    