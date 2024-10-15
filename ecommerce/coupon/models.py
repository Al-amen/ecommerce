from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from store.models import Product




class Coupon(models.Model):

    code = models.CharField(max_length=15,unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(70)])
    active = models.BooleanField(default=False)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
       
        verbose_name = 'Coupon Code'
        
    
    def __str__(self):
        return self.code



