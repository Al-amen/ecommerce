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
            color = request.POST.get('color')
            size = request.POST.get('size')
            quantiy = request.POST.get('quantity')
            if quantiy:
                order_item[0].quantity += int(quantiy)
            else:
               order_item[0].quantity += 1

            order_item[0].color = color
            order_item[0].size = size
            order_item[0].save()
            return redirect("store:index")
        else:
            color = request.POST.get('color')
            size = request.POST.get('size')
            
            order_item[0].color = color
            order_item[0].size = size
            order.order_items.add(order_item[0])
            return redirect('store:index')

    else:
        order = Order(user=request.user)
        order.save()
        order.order_items(order_item[0])
        return redirect('store:index')


def cart_view(request):
    carts = Cart.objects.filter(user=request.user,purchased=False)
    orders = Order.objects.filter(user=request.user,ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]

        context= {
            'carts':carts,
            'order':order
        }

        return render(request, 'store/cart.html', context=context)
  
def remove_item_from_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.order_items.remove(order_item)
            order_item.delete()
            return redirect('order:cart_veiw')
        else:
            return redirect('order:cart_view')
    else:
        return redirect('order:cart_view')

