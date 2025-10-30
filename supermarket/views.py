from django.shortcuts import render, redirect
from products.models import Products

def home(request):
    user = request.user
    products = Products.objects.all()
    return render(request ,"home.html",
        context={
            "products": products
        })

    