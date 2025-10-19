from django.shortcuts import render, redirect
from django.http import request, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url='market:login')
def home(request):
    user = User.objects.get(username="gabigol")
    cart_price = user.cart.total_price
    return render(request ,"home.html", context={"user": user, "cart_price": cart_price})