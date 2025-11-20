from product.models import Product
from cart.models import Cart, CartItem
from inventory.models import InventoryItem

def add_to_cart(request):
    user = request.user
    cart = user.cart
    id = request.POST.get("id")
    quantity = int(request.POST.get("quantity"))
    product = Product.objects.get(id=id)
    
    if product.discount:
        discount_amount = (product.price * product.discount.discount) / 100
        final_price = product.price - discount_amount
    else:
        final_price = product.price
        
    stock = product.stocks.first()
    if stock and stock.quantity >= 1:
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity,})
        
        if not created:
            item.quantity += quantity
            item.save()
    return id
    

def cartremove(request):
    id = request.POST.get("id")
    user = request.user
    cart = user.cart
    cart.items.filter(id=id).delete()