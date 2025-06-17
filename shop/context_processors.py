

def cart_count_processor(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if isinstance(cart, dict) else 0
    return {'cart_count': cart_count}
