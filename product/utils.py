from product.models import Product
from cart.models import CartItem
from product.models import Variation

def get_flag(request):
    user = request.user
    cart = user.cart
    id = request.POST.get("id")
    product = Product.objects.get(id=id)
    variant = product.variations.first()
    item = CartItem.objects.get(cart=cart, product=product, variant=variant, defaults={'quantity': quantity,})
    if item.quantity == variant.stock:
        return False    