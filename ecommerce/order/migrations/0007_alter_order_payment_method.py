# Generated by Django 5.1.2 on 2024-10-20 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('SSLcommerz', 'SSLcommerz'), ('PayPal', 'PayPal')], default='Cash on Delivery', max_length=30),
        ),
    ]
