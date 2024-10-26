#store app/ views.py

from django.db.models import Avg, Count
from django.shortcuts import render
from django.views.generic import ListView,DetailView,TemplateView
from store.models import (Product,ProductImages,VariationValue,Banner)
from review.models import Review,ReviewImage                         
from store.models import Product,Category                     

class HomemplateView(TemplateView):
    template_name = 'store/index.html'  # Specify your template here

    def get(self, request, *args, **kwargs):
        products = Product.objects.all().annotate(
            average_rating=Avg('reviews__rating'),  # Calculate average rating
            review_count=Count('reviews')           # Count the number of reviews
        ).order_by('id')
        banners = Banner.objects.filter(is_active=True).order_by('-id')[:3]

        context = {
            'products': products,
            'banners': banners,
        } 
        
        return render(request, self.template_name, context=context)
   

from django.db.models import Q

class SearchResultsView(TemplateView):
    template_name = 'store/search_results.html'  # Specify the template name

    def get(self, request, *args, **kwargs):
        search_product = request.GET.get('search_product')
        category_id = request.GET.get('category')
        subcategory_id = request.GET.get('subcategory')

        products = Product.objects.all()

        if search_product:
            products = products.filter(
                Q(name__icontains=search_product) | 
                Q(category__name__icontains=search_product)
            )

        if category_id:
            # Filter products by category
            products = products.filter(category_id=category_id)
        elif subcategory_id:
            # Filter products by subcategory
            products = products.filter(category_id=subcategory_id)

        context = {
            'products': products.order_by('id'),
            'search_term': search_product,
        }
        return self.render_to_response(context)

class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch product images, color, and size variations
        context["product_images"] = ProductImages.objects.filter(product=self.object.id)
        context["color_variations"] = VariationValue.objects.colors().filter(product=self.object)
        context["size_variations"] = VariationValue.objects.sizes().filter(product=self.object)

        # Fetch the reviews related to this product
        reviews = Review.objects.filter(product=self.object).select_related('user')
        context["reviews"] = reviews
         # Calculate average rating for the product
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        context["average_rating"] = average_rating if average_rating else 0 
        

        print("size Variations: ", context["size_variations"])
        return context

    

