from urllib import response
from django.shortcuts import redirect
from product.models import Product
from cart.models import CartItem
from django.http import HttpResponse
import requests
from payment.utils import create_checkout_session_product


def add_to_cart(request):
    user = request.user
    cart = user.cart
    id = request.POST.get("id")
    quantity = int(request.POST.get("quantity"))
    product = Product.objects.get(id=id)
    stock = product.stocks.first()
    if stock and stock.quantity >= 1:
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity,})
        if not created:
            item.quantity += quantity
            item.save()
    return id
    

def cartremove(request):
    try:
        id = request.POST.get("id")
        user = request.user
        cart = user.cart
        cart.items.filter(id=id).delete()
    except Exception as e:
        return HttpResponse(status=200)
    
    
def cartbuy(request):
    form = request.POST.dict()
    response = validade_cep(form["cep"])
    print(form)
    print(response)
    return redirect("market:home")
    user = request.user
    urls = {"success_url": "inventory/", "cancel_url": "cart/"} 
    line_items = [
            {
                "price_data": {
                    "currency": "brl",
                    "unit_amount": int((item.product.apply_discount()) * 100),
                    "product": item.product.id_stripe,
                },
                "quantity": item.quantity
            }
        for item in user.cart.items.all()]
    
    metadata={
        "cart_id": str(user.cart.id),
        "user_id": str(user.id),
    }
    return redirect(create_checkout_session_product(metadata, line_items, urls))



def validade_cep(cep):
    cep = cep
    url= f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return (content := response.json())
    except requests.exceptions.Timeout: 
        return "Timeout"
    except requests.exceptions.HTTPError as e:
        return "Error"