# Generated by Django 5.2.3 on 2025-06-16 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_city_order_shipping_fee_order_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('vodafone', 'Vodafone Cash'), ('instapay', 'InstaPay'), ('Cash on Delivery', 'Cash on Delivery')], default='cod', max_length=20),
        ),
    ]
