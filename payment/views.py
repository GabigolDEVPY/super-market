from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from product.models import Product
from django.contrib.auth.models import User
from accounts.models import Inventory, InventoryItem
from .models import Order
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


        
class PaymentsHome(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = "Payments.html"
    context_object_name = "orders"
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    
    
    