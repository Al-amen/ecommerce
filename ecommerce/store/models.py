#store app / models.py



from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model



#category model
class Category(models.Model):

    name = models.CharField(max_length=50, blank=False, null=False)
    image = models.ImageField(upload_to="category", blank=True, null=True)
    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Categories'


    def get_total_stock(self):
        """Calculate total stock for the category and its subcategories."""
        products = Product.objects.filter(category__in=self.get_descendants(include_self=True))
        total_stock = sum(product.stock for product in products)
        return total_stock

    def get_descendants(self, include_self=True):
        """Helper method to get all subcategories including self."""
        categories = [self]
        for child in self.children.all():
            categories.extend(child.get_descendants(include_self=True))
        return categories if include_self else categories[1:]


class Product(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    preview_des = models.CharField(
        max_length=255, verbose_name="Short Descriptions")
    description = models.TextField(
        max_length=1000, verbose_name="Descriptions")
    image = models.ImageField(upload_to='products', blank=False, null=False)
    price = models.FloatField()
    old_price = models.FloatField(default=0.00, blank=True, null=True)
    is_stock = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)  
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.name

    class Meta:

        ordering = ['-created']
    
    def get_product_url(self):
        return reverse("store:product_detail", kwargs={"slug": self.slug})
    
    
    def save(self, *args, **kwargs):
        # Set stock status based on stock count
        self.is_stock = self.stock > 0
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    

    def decrease_stock(self, quantity=1):
        """Decrease stock by specified quantity when product is sold."""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
        else:
            self.is_stock = False
            raise ValueError("Insufficient stock for this product")


class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.FileField(upload_to='product_gellary')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.product.name)
    

class VariationManger(models.Manager):
    def sizes(self):
        return super(VariationManger,self).filter(variation='size')
    
    def colors(self):
        return super(VariationManger,self).filter(variation='color')
        





VARIATIONS_TYPE = (
    ('size','size'),
    ('color','color'),
)



class VariationValue(models.Model):
    variation = models.CharField(max_length=100,choices=VARIATIONS_TYPE)
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField()
    image = models.ImageField(upload_to='variations',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)  
    is_stock = models.BooleanField(default=True)

    objects = VariationManger()

    def __str__(self):
        return self.name
    
    def decrease_stock(self, quantity=1):
        """Decrease stock by specified quantity for variation when sold."""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
        else:
            self.is_stock = False
            raise ValueError("Insufficient stock for this variation")

class Banner(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='banner')
    image = models.ImageField(upload_to='banner')
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.name
    


User = get_user_model()

class MyLogo(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   image = models.ImageField(unique='logo')
   is_active=models.BooleanField(default=True)
   is_created = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return str(self.image)



class MyFavicon(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   image=models.ImageField(upload_to='favicon')
   is_active = models.BooleanField(default=False)
   is_created = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return str(self.image)
