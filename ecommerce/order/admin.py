from django.contrib import admin

from order import models

admin.site.register(models.Cart)
admin.site.register(models.Order)