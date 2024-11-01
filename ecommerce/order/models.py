#order app / models.py

from django.db import models
from django.contrib.auth import get_user_model
from store.models import Product,VariationValue
from django.conf import settings
from django.core.mail import send_mail
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
        return f"{self.quantity} X {self.item.name}"

    def get_total(self):
        return format(self.item.price * self.quantity, '0.2f')

    def variation_single_price(self):
        sizes = VariationValue.objects.filter(variation='size', product=self.item)
        colors = VariationValue.objects.filter(variation='color', product=self.item)

        c_price = 0
        if colors.exists() and self.color:
            color_obj = colors.filter(name=self.color).first()
            c_price = color_obj.price if color_obj else 0

        if sizes.exists() and self.size:
            size_obj = sizes.filter(name=self.size).first()
            size_price = size_obj.price if size_obj else 0
            total = size_price + c_price
            return format(total, '.2f')

        return format(self.item.price, '.2f')  # Fallback to base product price

    # def variation_total(self):
    #     sizes = VariationValue.objects.filter(variation='size', product=self.item)
    #     colors = VariationValue.objects.filter(variation='color', product=self.item)

    #     total = 0
    #     color_quantity_price = 0

    #     if colors.exists() and self.color:
    #         color_obj = colors.filter(name=self.color).first()
    #         color_quantity_price = (color_obj.price * self.quantity) if color_obj else 0

    #     if sizes.exists() and self.size:
    #         size_obj = sizes.filter(name=self.size).first()
    #         if size_obj:
    #             total = (size_obj.price * self.quantity)

    #     net_total = total + color_quantity_price
    #     return format(net_total, '0.2f')


    def variation_total(self):
        sizes = VariationValue.objects.filter(variation='size', product=self.item)
        colors = VariationValue.objects.filter(variation='color', product=self.item)

        if not (self.color or self.size):
            return 0  # No variation selected, return None

        total = 0
        color_quantity_price = 0

        if colors.exists() and self.color:
            color_obj = colors.filter(name=self.color).first()
            color_quantity_price = (color_obj.price * self.quantity) if color_obj else 0

        if sizes.exists() and self.size:
            size_obj = sizes.filter(name=self.size).first()
            if size_obj:
                total = (size_obj.price * self.quantity)

        net_total = total + color_quantity_price
        return format(net_total, '0.2f')






#order model
class Order(models.Model):
    PAYMENT_METHOD = {
        ('Cash on Delivery','Cash on Delivery'),
        ('PayPal', 'PayPal'),
        ('SSLcommerz', 'SSLcommerz'),
    }

    SHIPPING_STATUS = {
        ('Pending', 'Pending'),
        ('Order Confirmed', 'Order Confirmed'),
        ('On the Way', 'On the Way'),
        ('Delivered', 'Delivered'),
    }

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_items = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    payment_id = models.CharField(max_length=255,blank=True,null=True)
    order_id = models.CharField(max_length=255,blank=True,null=True)
    payment_method = models.CharField(max_length=30,choices=PAYMENT_METHOD,default='Cash on Delivery')
    shipping_status = models.CharField(max_length=20, choices=SHIPPING_STATUS, default='Pending')

    def get_totals(self):
        total = 0
        for order_item in self.order_items.all():
           
      
         if order_item.variation_total() and float(order_item.variation_total()) > 0:
            item_total = float(order_item.variation_total())
         elif order_item.variation_single_price() and float(order_item.variation_single_price()) > 0:
            item_total = float(order_item.variation_single_price())
         else:
            
            item_total = float(order_item.get_total())

      
        total += item_total
    

      
        return total
    
    def get_ordered_items(self):
        """
        Returns a list of ordered items with their quantity, name, and total price.
        """
        items = []
        for item in self.order_items.all():
            product_info = {
                'product_name': item.item.name,
                'quantity': item.quantity,
                'total_price': item.get_total()
            }
            items.append(product_info)
        return items
    
    
    def save(self, *args, **kwargs):
        # Send email when shipping status is updated
        if self.pk:
            old_order = Order.objects.get(pk=self.pk)
            if old_order.shipping_status != self.shipping_status:
                self.send_status_email()
        super(Order, self).save(*args, **kwargs)

    
    def send_status_email(self):
        subject = f"Your Order #{self.order_id} Status Update"
        message = f"Dear {self.user.user_name},\n\nYour order status has been updated to '{self.shipping_status}'.\n\nThank you for shopping with us!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.user.email]

        send_mail(
            subject,
            message,
            from_email,  # Replace with your shop's email
            recipient_list,
            fail_silently=False,
        )
        
    


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