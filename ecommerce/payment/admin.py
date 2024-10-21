from django.contrib import admin
from payment.models import BillingAddress,Download
# Register your models here.

admin.site.register(BillingAddress)
admin.site.register(Download)