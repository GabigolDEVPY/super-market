from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from product.models import Product
from django.contrib.auth.models import User
from inventory.models import Inventory, InventoryItem


