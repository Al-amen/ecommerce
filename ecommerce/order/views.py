from django.shortcuts import render,get_object_or_404,redirect

from store.models import Product
from order.models import Cart,Order
from coupon.models import Coupon
from coupon.forms import CouponCodeForm
from django.utils import timezone

# Create your views here.

''''
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
'''

def add_to_cart(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Product, pk=pk)
        order_item, created = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]
            if order.order_items.filter(item=item).exists():
                color = request.POST.get('color')
                size = request.POST.get('size')
                quantity = request.POST.get('quantity')
                
                if quantity:
                    order_item.quantity += int(quantity)
                else:
                    order_item.quantity += 1

        
                order_item.color = color
                order_item.size = size
                order_item.save()

                return redirect("store:index")
            else:
            
                color = request.POST.get('color')
                size = request.POST.get('size')

                order_item.color = color
                order_item.size = size
                order_item.save()  

                order.order_items.add(order_item)  
                return redirect('store:index')
        else:
        
            new_order = Order.objects.create(user=request.user)
            new_order.order_items.add(order_item)  
            return redirect('store:index')
    else:
        return redirect('account:login')


'''def cart_view(request):
    carts = Cart.objects.filter(user=request.user,purchased=False)
    orders = Order.objects.filter(user=request.user,ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        coupon_form = CouponCodeForm(request.POST)

        if coupon_form.is_valid():
            current_time = timezone.now()
            code = coupon_form.cleaned_data.get('code')
            coupon_obj = Coupon.objects.get(code=code,active=True)

            if coupon_obj.valid_to >= current_time:
                get_discount = (coupon_obj.discount / 100) * order.get_totals()
                total_price_after_discount = order.get_totals() - get_discount
                request.session['discount_total'] = total_price_after_discount 
                request.session['coupon_code'] = code
                return redirect('order:cart')
            
            else:
                coupon_obj.active = False
                coupon_obj.save()
        total_price_after_discount = request.session.get('discount_total')
        coupon_code = request.session.get('coupon_code')
        context= {
            'carts':carts,
            'order':order,
            'coupon_form':coupon_form,
            'coupon_code':coupon_code,
            'total_price_after_discount':total_price_after_discount,
        }

        return render(request, 'store/cart.html', context=context)
'''




def cart_view(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)

        coupon_code = None
        total_price_after_discount = None
        order = None  
        coupon_form = None 

        if carts.exists() and orders.exists():
            order = orders[0]
            coupon_form = CouponCodeForm(request.POST or None)  

            if coupon_form.is_valid():
                current_time = timezone.now()
                code = coupon_form.cleaned_data.get('code')

                try:
                    coupon_obj = Coupon.objects.get(code=code, active=True)

                    if coupon_obj.valid_from <= current_time <= coupon_obj.valid_to:
                        
                        get_discount = (coupon_obj.discount / 100) * order.get_totals()
                        total_price_after_discount = order.get_totals() - get_discount
                        request.session['discount_total'] = total_price_after_discount 
                        request.session['coupon_code'] = code

                        coupon_code = code  
                    else:
                    
                        coupon_obj.active = False
                        coupon_obj.save()
                        coupon_code = None  
                except Coupon.DoesNotExist:
                
                    coupon_code = None

        if 'discount_total' in request.session:
            total_price_after_discount = request.session['discount_total']
            coupon_code = request.session.get('coupon_code')

        print("Current coupons in database:")
        for coupon in Coupon.objects.all():
            print(coupon.code, coupon.valid_from, coupon.valid_to, coupon.active)

        
        context = {
            'carts': carts,
            'order': order,  
            'coupon_form': coupon_form,  
            'coupon_code': coupon_code,
            'total_price_after_discount': total_price_after_discount,
        }

        return render(request, 'store/cart.html', context) 
    else:
        return redirect('account:login')






def remove_item_from_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.order_items.remove(order_item)
            order_item.delete()
            return redirect('order:cart')
        else:
            return redirect('order:cart')
    else:
        return redirect('order:cart')



def increase_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                return redirect('order:cart')
        else:
            return redirect('store:index')
    else :
        return redirect('store:index')
    



def decrease_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                return redirect('order:cart')
            else:
                order_item.order_items.remove(order_item)
                order_item.delete()
                return redirect('store:index')
        else:
            return redirect('store:index')
    else:
        return redirect('store:index')


