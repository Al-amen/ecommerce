from django.shortcuts import render,get_object_or_404,redirect

from store.models import Product
from order.models import Cart,Order
# Create your views here.


def add_to_cart(request,pk):
    
    item = get_object_or_404(Product,pk=pk)
    order_item = Cart.objects.get_or_create(item=item,user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            return redirect("store:index")
        else:
            order.order_items.add(order_item[0])
            return redirect('store:index')

    else:
        order = Order(user=request.user)
        order.save()
        order.order_items(order_item[0])
        return redirect('store:index')