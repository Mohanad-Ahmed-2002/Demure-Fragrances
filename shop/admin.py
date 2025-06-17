from django.contrib import admin
from .models import Product,ContactMessage,City,Order,OrderItem,PromoCode

admin.site.register(Product)

admin.site.register(ContactMessage)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'city', 'payment_method', 'total', 'shipping_fee', 'created_at')
    list_filter = ('payment_method', 'city', 'created_at')
    search_fields = ('full_name', 'phone', 'address')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')


admin.site.register(City)

admin.site.register(PromoCode)