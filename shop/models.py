from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = CloudinaryField('image')
    def __str__(self):
        return self.name
    image = CloudinaryField('image')

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


class City(models.Model):
    name = models.CharField(max_length=100)
    shipping_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Order(models.Model):

    PAYMENT_CHOICES = [
        ('vodafone', 'Vodafone Cash'),
        ('instapay', 'InstaPay'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ]


    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    shipping_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Cash on Delivery')  # ✅ جديد
    created_at = models.DateTimeField(auto_now_add=True)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def final_total(self):
        total_with_shipping = self.total + (self.city.shipping_fee if self.city else 0)
        return total_with_shipping - self.discount



    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # السعر وقت الطلب

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"


