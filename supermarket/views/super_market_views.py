from django.shortcuts import render, redirect
from django.http import request, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from supermarket.models import Cart

# Create your views here.

@login_required(login_url='market:login')
def home(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    items = cart.items.all()
    cart_price = user.cart.total_price
    return render(request ,"home.html", context={"user": user, "cart_price": cart_price, "items": items if items else "Nada"})