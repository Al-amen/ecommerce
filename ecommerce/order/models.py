#order app / models.py

from django.db import models
from django.contrib.auth import get_user_model
from store.models import Product,VariationValue

User = get_user_model()


#cart model
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    color = models.CharField(max_length=100, blank=True,null=True)
    size = models.CharField(max_length=100,blank=True,null=True)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.quantity} X {self.item}"
    

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total,'0.2f')

        return float_total
    
    def variation_single_price(self):
        sizes = VariationValue.objects.filter(variation='size', product=self.item)
        colors = VariationValue.objects.filter(variation='color', product=self.item)
        
        for size in sizes:
            if colors.exists():
                for color in colors:
                    if color.name == self.color:
                        c_price = color.price
                    
                if size.name == self.size:
                    total = size.price + c_price
                    net_total = total
                    float_total = format(net_total,'.2f')
                    return float_total
            else:
                if size.name == self.size:
                    total = size.price
                    float_total = format(total,'.2f')
                    return float_total

    def variation_total(self):
        sizes = VariationValue.objects.filter(variation='size', product=self.item)
        colors = VariationValue.objects.filter(variation='color', product=self.item)

        for size in sizes:
           if colors.exists():
               for color in colors:
                   if color.name == self.color:
                    c_price = color.price
                    color_quantity_price = c_price * self.quantity
                
               if size.name == self.size:
                   total = size.price * self.quantity
                   net_total = total + color_quantity_price
                   float_total = format(net_total,'0.2f')
                   return float_total
           else:
               if size.name == self.size:
                   total = size.price * self.quantity
                   float_total = format(total,'0.2f')
                   return float_total








#order model
class Order(models.Model):
    PAYMENT_METHOD = {
        ('Cash on Delivery','Cash on Delivery'),
        ('PayPal', 'PayPal'),
        ('SSLcommerz', 'SSLcommerz'),
    }

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_items = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    payment_id = models.CharField(max_length=255,blank=True,null=True)
    order_id = models.CharField(max_length=255,blank=True,null=True)
    payment_method = models.CharField(max_length=30,choices=PAYMENT_METHOD,default='Cash on Delivery')


    def get_totals(self):
        total = 0
        for order_item in self.order_items.all():
            if order_item.variation_total():
                total += float(order_item.variation_total())
            elif order_item.variation_single_price():
                total += float(order_item.variation_single_price())
            else:
                total += float(order_item.get_total())
        
        return total
    


    # WishList model
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_name} - {self.product.name}"

    class Meta:
        unique_together = ('user', 'product')  # Ensure the same product isn't added multiple times by the same user.
        ordering = ['-added_at']