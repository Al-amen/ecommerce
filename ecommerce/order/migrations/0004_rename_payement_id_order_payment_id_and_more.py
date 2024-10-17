# Generated by Django 5.1.2 on 2024-10-16 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_payment_method'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payement_id',
            new_name='payment_id',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('PayPal', 'PayPal'), ('SSLcommercez', 'SSLcommercez'), ('Cash on Delivery', 'Cash on Delivery')], default='Cash on Delivery', max_length=30),
        ),
    ]