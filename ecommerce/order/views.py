from django.shortcuts import render,get_object_or_404,redirect

from store.models import Product
from order.models import Cart,Order,WishList
from coupon.models import Coupon
from coupon.forms import CouponCodeForm
from django.utils import timezone
from notification.notific import SendNotification

# Create your views here.


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
                message = f"Quantity updated"
                SendNotification(request.user,message)
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
            message = f"product added to your cart"
            SendNotification(request.user,message)
            return redirect('store:index')
    else:
        return redirect('account:login')





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



def add_to_wishlist(request,pk):
    product = get_object_or_404(Product, pk=pk)
    wishlist_item, created = WishList.objects.get_or_create(user=request.user, product=product)
    
    if created:
        # If the product was added to the wishlist
        message = "Product added to wishlist."
    else:
        # If the product was already in the wishlist
        message = "Product is already in your wishlist."
    print(message)

    return redirect('order:view_wishlist')


def view_wishlist(request):
    wishlist_items = WishList.objects.filter(user=request.user)
    print(wishlist_items)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})


def remove_from_wishlist(request, pk):
    if request.user.is_authenticated:
        print(f"Trying to remove product with pk={pk} from wishlist for user {request.user}")
        wishlist_item = get_object_or_404(WishList, product__pk=pk, user=request.user)
        wishlist_item.delete()
        return redirect('order:view_wishlist')
    else:
        return redirect('account:login')


import os
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect
from order.models import Order
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def generate_invoice(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        # Get the order details
        order = get_object_or_404(Order, user=request.user, order_id=order_id)

        # Create a byte stream buffer to hold the PDF data
        buffer = BytesIO()

        # Create a PDF object and add content
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Invoice Header
        p.drawString(100, height - 50, "Invoice")
        p.drawString(100, height - 70, f"Order ID: {order.order_id}")
        p.drawString(100, height - 90, f"Date: {timezone.now().date()}")

        # Add Product Details
        y_position = height - 130
        p.drawString(100, y_position, "Ordered Products:")
        y_position -= 20

        for item in order.get_ordered_items():
            p.drawString(100, y_position, f"{item['quantity']} X {item['product_name']}")
            p.drawString(300, y_position, f"${item['total_price']}")
            y_position -= 20

        # Add Total
        p.drawString(100, y_position - 20, f"Total: ${order.get_totals()}")

        # Finalize the PDF
        p.showPage()
        p.save()

        # Get the PDF from the buffer
        pdf_data = buffer.getvalue()
        buffer.close()

        # Save the PDF to the media folder
        invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
        if not os.path.exists(invoice_dir):
            os.makedirs(invoice_dir)
        invoice_filename = f"invoice_{order_id}.pdf"
        invoice_path = os.path.join(invoice_dir, invoice_filename)
        with open(invoice_path, 'wb') as f:
            f.write(pdf_data)

        # Send the invoice via email
        email_subject = 'Your Invoice from Our Store'
        email_message = 'Please find attached your invoice.'
        email = EmailMessage(
            subject=email_subject,
            body=email_message,
            to=[request.user.email]
        )
        email.attach(invoice_filename, pdf_data, 'application/pdf')
        email.send()

        logger.info(f"Invoice for Order {order_id} has been generated and sent to {request.user.email}.")

        # Redirect to the index page
        return redirect(reverse('store:index'))

    except Exception as e:
        logger.error(f"Error generating invoice for order {order_id}: {e}")
        return HttpResponse("An error occurred while generating the invoice.", status=500)
