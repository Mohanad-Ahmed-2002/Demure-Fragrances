from django.shortcuts import render,get_object_or_404,redirect
from .models import ContactMessage,Product,Order, OrderItem, Product,City,PromoCode
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .forms import CheckoutForm
from django.core.serializers.json import DjangoJSONEncoder
import json


def home(request):
    return render(request, 'home.html')

def contact(request):
    success = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(name=name, email=email, message=message)
        success = True

    return render(request, 'contact.html', {'success': success})

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    # نتأكد إنها dict فعلًا
    if not isinstance(cart, dict):
        cart = {}

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    products = []
    grand_total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        total = product.price * qty
        grand_total += total
        products.append({
            'product': product,
            'quantity': qty,
            'total': total,
        })

    return render(request, 'cart.html', {
        'products': products,
        'grand_total': grand_total
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')

def update_quantity(request, product_id, action):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        if action == 'increase':
            cart[product_id] += 1
        elif action == 'decrease':
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')

@csrf_exempt
def ajax_add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not isinstance(cart, dict):
            cart = {}
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart

        cart_count = sum(cart.values())
        return JsonResponse({'cart_count': cart_count})

def cart_count_api(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if isinstance(cart, dict) else 0
    return JsonResponse({'cart_count': cart_count})

def add_to_favourites(request, product_id):
    favourites = request.session.get('favourites', [])
    if product_id not in favourites:
        favourites.append(product_id)
        request.session['favourites'] = favourites
    return redirect('shop')

def remove_from_favourites(request, product_id):
    favourites = request.session.get('favourites', [])
    if product_id in favourites:
        favourites.remove(product_id)
        request.session['favourites'] = favourites
    return redirect('favourites')

def favourites_view(request):
    favourites = request.session.get('favourites', [])
    products = Product.objects.filter(id__in=favourites)
    return render(request, 'favourites.html', {'products': products})

def checkout(request):
    cart = request.session.get('cart', {})
    products = []
    grand_total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        total = product.price * qty
        grand_total += total
        products.append({'product': product, 'quantity': qty, 'total': total})

    shipping_fee = 0
    promo_code = None
    discount = 0

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total = grand_total

            # التحقق من كود الخصم
            code = form.cleaned_data.get('promo_code', '').strip()
            if code:
                try:
                    promo_code = PromoCode.objects.get(code__iexact=code, is_active=True)
                    discount = promo_code.discount_amount
                    order.promo_code = promo_code
                    order.discount = discount
                except PromoCode.DoesNotExist:
                    pass

            shipping_fee = order.city.shipping_fee if order.city else 0
            order.shipping_fee = shipping_fee
            order.save()

            for item in products:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )

            request.session['cart'] = {}
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm()

    cities = City.objects.all()
    cities_dict = {str(city.id): float(city.shipping_fee) for city in cities}
    cities_json = json.dumps(cities_dict)

    return render(request, 'checkout.html', {
        'form': form,
        'products': products,
        'grand_total': grand_total,
        'cities_json': cities_json,
    })

def validate_promo(request):
    code = request.GET.get('code', '').strip()
    try:
        promo = PromoCode.objects.get(code__iexact=code, is_active=True)
        return JsonResponse({'valid': True, 'discount': float(promo.discount_amount)})
    except PromoCode.DoesNotExist:
        return JsonResponse({'valid': False})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})
