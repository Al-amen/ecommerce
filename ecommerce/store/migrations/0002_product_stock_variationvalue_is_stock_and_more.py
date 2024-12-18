# Generated by Django 5.1.2 on 2024-10-26 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='variationvalue',
            name='is_stock',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='variationvalue',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
