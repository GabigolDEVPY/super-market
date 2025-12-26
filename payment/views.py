from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from payment.utils import paymentbuy
from product.models import Product
from django.contrib.auth.models import User
from accounts.models import Inventory, InventoryItem
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


        
class PaymentValidate(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "index.html")
    
class PaymentBuy(LoginRequiredMixin, View):
    def post(self, request):
        paymentbuy(request)