# Generated by Django 5.1.2 on 2024-10-17 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_rename_ordee_id_order_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('SSLcommerz', 'SSLcommerz'), ('Cash on Delivery', 'Cash on Delivery'), ('PayPal', 'PayPal')], default='Cash on Delivery', max_length=30),
        ),
    ]
