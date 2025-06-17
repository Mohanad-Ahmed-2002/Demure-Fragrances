from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        widget=forms.RadioSelect
    )

    promo_code = forms.CharField(
        required=False,
        label="Promo Code",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2  transition',
            'placeholder': 'Promo Code',
            'id': 'id_promo_code'
        })
    )

    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'city', 'address', 'notes', 'payment_method']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2  transition',
                'placeholder': 'Full Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2  transition',
                'placeholder': 'Phone Number'
            }),
            'city': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2  transition',
                'id': 'id_city'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2  transition',
                'placeholder': 'Address',
                'rows': 3
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2  transition',
                'placeholder': 'Notes (Optional)',
                'rows': 2
            }),
        }
