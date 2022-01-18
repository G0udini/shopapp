from .cart import Cart


def cart(request):
    cart = Cart(request)
    cart.find_coupon()
    return {"cart": cart}
