#store app/ views.py


from django.shortcuts import render
from store import models
from django.views.generic import ListView,DetailView


class HomeListView(ListView):
    model = models.Product
    template_name = 'store/index.html'
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = models.Product
    template_name = "store/product.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_images"] = models.ProductImages.objects.filter(product=self.object.id)

        context["color_variations"] = models.VariationValue.objects.colors().filter(product=self.object)
        context["size_variations"] = models.VariationValue.objects.sizes().filter(product=self.object)
        
        print(" size Variations: ",   context["size_variations"])
        return context
    

