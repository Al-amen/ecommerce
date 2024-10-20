from django.db import models
from django.contrib.auth import get_user_model
from store.models import Product
from order.models import Order

User = get_user_model()

# Review model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")  # User can have many reviews
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")  # Product can have many reviews
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="reviews", blank=True, null=True)  # Ensure the review is linked to a completed order
    rating = models.PositiveIntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    title = models.CharField(max_length=255, blank=True, null=True)
    review_text = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.product.name}"

    class Meta:
        unique_together = ('user', 'product', 'order')  # Ensure one review per product per order
        
    def is_order_completed(self):
        # Check if the related order is marked as completed
        return self.order.ordered

    def save(self, *args, **kwargs):
        # Ensure the order is completed before saving the review
        if not self.is_order_completed():
            raise ValueError("Cannot review a product unless the order is completed.")
        super().save(*args, **kwargs)


# ReviewImage model (for multiple images)
class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images")  # Each review can have many images
    image = models.ImageField(upload_to="review_images/")  # Store images in review_images/ directory
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.review.product.name} by {self.review.user.username}"
