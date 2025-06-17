"""
URL configuration for perfume_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # ✅ هنا
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:product_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('ajax/add-to-cart/<int:product_id>/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
    path('api/cart-count/', views.cart_count_api, name='cart_count_api'),
    path('checkout/', views.checkout, name='checkout'),
    path('api/validate-promo/', views.validate_promo, name="validate_promo"),
    path('order-success/<int:order_id>/', views.order_success, name="order_success"),
    path('favourites/', views.favourites_view, name='favourites'),
    path('add-to-favourites/<int:product_id>/', views.add_to_favourites, name='add_to_favourites'),
    path('remove-from-favourites/<int:product_id>/', views.remove_from_favourites, name='remove_from_favourites'),







]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

