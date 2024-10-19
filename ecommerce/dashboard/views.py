from django.shortcuts import render,redirect

from django.views.generic import TemplateView, ListView
from django.views.generic.edit import DeleteView

from store.models import Category, Product
from store.forms import (
    ProductForm,
    CategoryForm
)

class DashboardIndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/index.html')
    

    def post(self, request, *args, **kwargs):
        pass


# product view
class ProductListView(TemplateView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '') 
        products = Product.objects.all().order_by('-id')

        if query:
            products = Product.objects.filter(name__icontains=query).order_by('-id')
        else:
            products = Product.objects.all().order_by('-id')

        context = {
            'products': products,
            'search_query': query,
        }
        return render(request, 'dashboard/product_list.html', context)


    def post(self, request, *args, **kwargs):
        pass



#add new product
class AddNewProduct(TemplateView):
    template_name = 'dashboard/add_form.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 'developer':
                form = ProductForm()
                context = {
                    'form': form
                }
                return render(request, self.template_name, context)
            else:
                return redirect('store:index')
            
            return redirect('account:profile')
        else:
            return redirect('store:index')
        

    def post(self, request, *args, **kwargs):
        if request.user.user_type == 'developer':
            if request.method == 'post' or request.method == 'POST':
                form = ProductForm(request.POST, request.FILES)
                if form.is_valid():
                    product = form.save(commit=False)
                    slug = product.name.replace(' ', '-')
                    product.slug = slug.lower()
                    product.save()
                    return redirect('dashboard:product_list')

                    
            else:
                return redirect('store:index')
        else:
            return redirect('store:index')


#updateview
class ProductUpdateView(TemplateView):
    def get(self, request, slug, *args, **kwargs):
        product = Product.objects.get(slug=slug)
        form = ProductForm(instance=product)
        context = {
            'form': form
        }
        return render(request, 'dashboard/add_form.html', context)

    def post(self, request, slug, *args, **kwargs):
        if request.user.user_type == 'developer':
            if request.method == 'post' or request.method == 'POST':
                product_ins = Product.objects.get(slug=slug)
                form = ProductForm(request.POST, request.FILES, instance=product_ins)
                if form.is_valid():
                    product = form.save(commit=False)
                    slug = product.name.replace(' ', '-')
                    product.slug = slug.lower()
                    product.save()
                    return redirect('dashboard:product_list')

                    
            else:
                return redirect('store:index')
        else:
            return redirect('store:index')
        

#product delete
class ProductDeleteView(TemplateView):
    def get(self, request, slug, *args, **kwargs):
        product = Product.objects.get(slug=slug)
        product.delete()
        return redirect('dashboard:product_list')



# category view
class CategoryListView(ListView):
    model = Category
    template_name = 'dashboard/category_list.html'
    context_object_name = 'categories'




#add new category
class AddNewCategory(TemplateView):
    def get(self, request, *args):
        if request.user.user_type == 'developer':
            form = CategoryForm()
            context = {
                'form': form
            }
            return render(request, 'dashboard/add_form.html', context)
        else:
            return redirect('store:index')

    def post(self, request, *args, **kwargs):
        if request.user.user_type == 'developer':
            if request.method == 'post' or request.method == 'POST':
                form = CategoryForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    return redirect('dashboard:category')

                    
            else:
                return redirect('store:index')
        else:
            return redirect('store:index')


#update category
class CategoryUpdateView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(id=pk)
        form = CategoryForm(instance=category)
        context = {
            'form': form
        }
        return render(request, 'dashboard/add_form.html', context)

    def post(self, request, pk, *args, **kwargs):
        if request.user.user_type == 'developer':
            if request.method == 'post' or request.method == 'POST':
                category = Category.objects.get(id=pk)
                form = CategoryForm(request.POST, request.FILES, instance=category)
                if form.is_valid():
                    form.save()
                    return redirect('dashboard:category')
            else:
                return redirect('store:index')
        else:
            return redirect('store:index')


#delete cetegory
class CategoryDeleteView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(id=pk)
        category.delete()
        return redirect('dashboard:category')