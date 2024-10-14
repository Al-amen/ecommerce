from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.quantity} X {self.item}"
    

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total,'0.2f')

        return float_total


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_items = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    payement_id = models.CharField(max_length=255,blank=True,null=True)
    ordee_id = models.CharField(max_length=255,blank=True,null=True)

    def get_totals(self):
        total = 0
        for order_item in self.order_items:
            total += float(order_item.get_total())
        
        return total