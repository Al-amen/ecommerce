# Generated by Django 5.1.2 on 2024-10-21 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_order_shipping_status_alter_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('SSLcommerz', 'SSLcommerz'), ('PayPal', 'PayPal'), ('Cash on Delivery', 'Cash on Delivery')], default='Cash on Delivery', max_length=30),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('On the Way', 'On the Way'), ('Order Confirmed', 'Order Confirmed'), ('Pending', 'Pending')], default='Pending', max_length=20),
        ),
    ]
