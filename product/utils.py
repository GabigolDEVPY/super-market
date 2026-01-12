from product.models import Product
from cart.models import CartItem
from product.models import Variation
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from requests import session
from product.models import Product
from django.views.generic.detail import DetailView
from product.models import DiscountCode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator
from payment.utils import create_checkout_session_product
from django.http import Http404

