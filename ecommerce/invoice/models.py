from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from order.models import Order
User = get_user_model()


class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='downloads')
    file = models.FileField(upload_to='invoices/')
    created_at = models.DateTimeField(auto_now_add=True)