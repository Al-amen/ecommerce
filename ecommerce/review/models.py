# review/models.py

from django.db import models
from django.conf import settings
from store.models import Product
from order.models import Order

User = settings.AUTH_USER_MODEL

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name="reviews", null=True, blank=True)
    review_text = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product', 'order')  # A user can review a product only after paying for it
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.user_name}'s review of {self.product.name}"

# ReviewImage model remains unchanged
class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="review_images/", blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
