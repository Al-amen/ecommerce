#store app/ views.py


from django.shortcuts import render
from django.views.generic import ListView,DetailView,TemplateView
from store.models import (Product,ProductImages,VariationValue,Banner)
                          
                       

class HomemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('id')
        banners = Banner.objects.filter(is_active=True).order_by('-id')[0:3]
        
        context = {
            'products':products,
            'banners':banners,
        }
        
        return render(request,'store/index.html',context=context)
    
    # def post(self, request, *args, **kwargs):
    #       if request.method == 'POST' or request.method == "post":
    #           search_product = request.POST.get('search_product')
    #           products = Product.objects.filter(name__icontains=search_product).order_by('id')

    #           context = {
    #                 'products':products
    #           }
    #           return render(request,'store/index.html',context=context)


class SearchResultsView(TemplateView):
    def post(self, request, *args, **kwargs):
        search_product = request.POST.get('search_product')
        products = Product.objects.filter(name__icontains=search_product).order_by('id')

        context = {
            'products': products,
            'search_term': search_product,
        }
        return render(request, 'store/search_results.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_images"] = ProductImages.objects.filter(product=self.object.id)

        context["color_variations"] = VariationValue.objects.colors().filter(product=self.object)
        context["size_variations"] = VariationValue.objects.sizes().filter(product=self.object)
        
        print(" size Variations: ",   context["size_variations"])
        return context
    

