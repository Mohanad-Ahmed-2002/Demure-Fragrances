from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ContactMessage, City, Order, OrderItem, PromoCode

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'quantity', 'price']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'city', 'payment_method', 'total', 'created_at', 'print_invoice_link')
    list_filter = ('payment_method', 'city', 'created_at')
    search_fields = ('full_name', 'phone', 'address')
    inlines = [OrderItemInline]

    def print_invoice_link(self, obj):
        return format_html(
            '<a href="/print-invoice/{}/" target="_blank" class="button">🧾 Print Invoice</a>', obj.id
        )

    print_invoice_link.short_description = 'Invoice'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

admin.site.register(Product)
admin.site.register(ContactMessage)
admin.site.register(City)
admin.site.register(PromoCode)
